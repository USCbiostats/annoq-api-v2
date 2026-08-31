# rsID Search Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make rsID search case- and whitespace-insensitive so that `RS1632919`, `Rs1632919` and `" rs1632919 "` return the same results as `rs1632919`, instead of silently returning zero.

**Architecture:** Two small module-level helpers in `helper_resolver.py` normalize caller input (strip + lower-case) and target the exact `rs_dbSNP.keyword` sub-field instead of the analyzed `text` field. Applied at all four rsID query sites — single and list, HRC and non-HRC. No change to the HRC subset clause, coordinate handling, response shape, or generated models.

**Tech Stack:** Python 3, FastAPI + Strawberry GraphQL, Elasticsearch 8.5, pytest 9.1.1.

## Global Constraints

- Run everything from the repo root `/home/muruganu/projects/temp/top_med/annoq-api-v2` with the venv active: `source venv/bin/activate`.
- **`src/routers/snp_router_helpers.py:12` must NOT change.** It uses `settings.DATA_RSID` to build a `_source` **projection** list, not a query. Appending `.keyword` there would request a sub-field that is absent from `_source`, silently dropping the field from responses.
- `rs_dbSNP` is mapped `text` with a `.keyword` sub-field (`ignore_above: 10000`). Term queries must target `.keyword`; `_source` projections must not.
- Do not switch to a `match` query. `match` is analyzed, so if `rs_dbSNP` ever became multi-valued it would silently start matching any token. `.keyword` fails loudly instead.
- Do not modify `src/graphql/resolvers/hrc.py` — this change is not HRC-specific.
- Do not modify `src/config/settings.py`. `DATA_RSID_COL` stays the bare field name; `.keyword` is appended at the query site.
- Generated models (`src/graphql/models/generated/`) and `scripts/class_generators/generated_schemas/` are **gitignored build artifacts** — never commit them.
- Per `CLAUDE.md`: resolver/query changes require `pytest` coverage and verification of real queries in the GraphQL playground.

**Spec:** `docs/superpowers/specs/2026-08-31-rsid-case-normalization-design.md`

---

## File Structure

| Path | Responsibility | Task |
|---|---|---|
| `src/graphql/resolvers/helper_resolver.py` | Add `_rsid_field()` + `_normalize_rsid()`; use them at 4 query sites | 1 |
| `test/unit/test_query_builders_hrc.py` | Update 3 existing assertions; add 4 normalization cases | 1 |
| `.env-example` | Document the two incompatible uses of `DATA_RSID_COL` | 2 |
| `docs/superpowers/specs/2026-07-15-hrc-search-design.md` | Correct 6 stale `HRC_rs_dbSNP151` references + header note | 2 |

---

### Task 1: rsID normalization in the query builders

**Files:**
- Modify: `src/graphql/resolvers/helper_resolver.py` (add 2 helpers above `rsID_query`; change 4 call sites at lines 211, 220, 250, 256)
- Test: `test/unit/test_query_builders_hrc.py`

**Interfaces:**
- Consumes: `settings.DATA_RSID` (already imported at `helper_resolver.py:3` as `from src.config.settings import settings`); `hrc.mapped_in_hrc_clause()` (already imported at line 20) — unchanged by this task.
- Produces:
  - `_rsid_field() -> str` — returns `f"{settings.DATA_RSID}.keyword"`
  - `_normalize_rsid(rsID: str) -> str` — returns `rsID.strip().lower()`
  - Both module-private to `helper_resolver.py`; no other module imports them.

- [ ] **Step 1: Write the failing tests**

In `test/unit/test_query_builders_hrc.py`, add this constant immediately below the existing `MAPPED = {"term": {"Mapped_in_HRC.keyword": "Y"}}` line:

```python
RSID_FIELD = f"{settings.DATA_RSID}.keyword"
```

Then **replace** the three existing rsID tests (currently at lines 46–74, between the `# --- rsID / rsIDs ---` banner and the `# --- IDs (VCF file) ---` banner) with:

```python
# --- rsID / rsIDs ----------------------------------------------------------
def test_rsID_query_without_hrc_uses_primary_rsid_field():
    assert rsID_query("rs123") == {
        "bool": {"filter": [{"term": {RSID_FIELD: "rs123"}}]}
    }


def test_rsID_query_with_hrc_uses_primary_rsid_field_and_subset_clause():
    # The raw HRC rsID is not carried; HRC rsID search uses rs_dbSNP + Mapped_in_HRC=Y.
    assert rsID_query("rs123", search_hrc=True) == {
        "bool": {
            "filter": [
                {"term": {RSID_FIELD: "rs123"}},
                MAPPED,
            ]
        }
    }


def test_rsIDs_query_with_hrc_uses_primary_rsid_field():
    assert rsIDs_query(["rs1", "rs2"], search_hrc=True) == {
        "bool": {
            "filter": [
                {"terms": {RSID_FIELD: ["rs1", "rs2"]}},
                MAPPED,
            ]
        }
    }


# rs_dbSNP is a `text` field, so an un-analyzed term query against the bare field is
# case-sensitive: "RS123" silently matched nothing. Input is normalized instead.
def test_rsID_query_normalizes_case_without_hrc():
    assert rsID_query("RS123") == {
        "bool": {"filter": [{"term": {RSID_FIELD: "rs123"}}]}
    }


def test_rsID_query_normalizes_case_and_whitespace_with_hrc():
    assert rsID_query("  Rs123  ", search_hrc=True) == {
        "bool": {
            "filter": [
                {"term": {RSID_FIELD: "rs123"}},
                MAPPED,
            ]
        }
    }


def test_rsIDs_query_normalizes_each_id_without_hrc():
    assert rsIDs_query(["rs1", "RS2", " Rs3 "]) == {
        "bool": {"filter": [{"terms": {RSID_FIELD: ["rs1", "rs2", "rs3"]}}]}
    }


def test_rsIDs_query_normalizes_each_id_with_hrc():
    assert rsIDs_query(["RS1", " rs2 "], search_hrc=True) == {
        "bool": {
            "filter": [
                {"terms": {RSID_FIELD: ["rs1", "rs2"]}},
                MAPPED,
            ]
        }
    }
```

- [ ] **Step 2: Run the tests to verify they fail**

```bash
source venv/bin/activate
pytest test/unit/test_query_builders_hrc.py -v -k rsID
```

Expected: **FAIL**. The three updated tests fail because the builders still emit the bare `rs_dbSNP` field rather than `rs_dbSNP.keyword`; the four new tests fail because no normalization happens. Failure messages compare dicts differing in the field key and/or the value's case.

- [ ] **Step 3: Add the two helpers**

In `src/graphql/resolvers/helper_resolver.py`, insert immediately **above** `def rsID_query(...)`:

```python
def _rsid_field() -> str:
    """Exact-match sub-field for rsID lookups.

    `rs_dbSNP` is mapped as `text`, so a term query against the bare field is matched
    against analyzed (lower-cased) tokens and is therefore case-sensitive in practice —
    "RS123" silently returns zero hits. Match the raw value via `.keyword` instead, and
    normalize the caller's input to suit (see _normalize_rsid).

    NOTE: this is for QUERIES only. `settings.DATA_RSID` is also used as a `_source`
    projection name in src/routers/snp_router_helpers.py, where `.keyword` must NOT be
    appended — sub-fields are absent from `_source`.
    """
    return f"{settings.DATA_RSID}.keyword"


def _normalize_rsid(rsID: str) -> str:
    """Normalize user-supplied rsID input for exact `.keyword` matching.

    dbSNP rsIDs are stored lower-case with no surrounding whitespace. Users paste them
    from papers and spreadsheets, which commonly introduces upper-case ("RS1632919") or
    padding; both return zero hits against `.keyword` without this.
    """
    return rsID.strip().lower()
```

- [ ] **Step 4: Use the helpers at all four query sites**

Line numbers below are pre-edit; inserting the helpers in Step 3 shifts them down. **Match on the code text, not the line number.**

In `rsID_query` — both the `search_hrc` branch (was line 211) and the `else` branch (was line 220) contain the identical line:

```python
                    {"term": {settings.DATA_RSID: rsID}},
```

Replace **both occurrences** with:

```python
                    {"term": {_rsid_field(): _normalize_rsid(rsID)}},
```

In `rsIDs_query`, the `search_hrc` branch (was line 250):

```python
                    {"terms": {settings.DATA_RSID: rsIDs}},
```

becomes:

```python
                    {"terms": {_rsid_field(): [_normalize_rsid(r) for r in rsIDs]}},
```

and the `else` branch (was line 256):

```python
        query = {"bool": {"filter": [{"terms": {settings.DATA_RSID: rsIDs}}]}}
```

becomes:

```python
        query = {"bool": {"filter": [{"terms": {_rsid_field(): [_normalize_rsid(r) for r in rsIDs]}}]}}
```

Verify exactly four replacements were made and none were missed:

```bash
grep -n "settings.DATA_RSID" src/graphql/resolvers/helper_resolver.py
```

Expected: **only** the `_rsid_field()` definition line. Any other hit is a missed call site.

- [ ] **Step 5: Run the tests to verify they pass**

```bash
pytest test/unit/test_query_builders_hrc.py -v
```

Expected: all tests PASS, including the non-rsID ones (chromosome, gene, IDs) which must be unaffected.

- [ ] **Step 6: Run the full unit suite for regressions**

```bash
pytest test/unit -v
```

Expected: all PASS. `test/integration/test_module_query.py:178-179` uses `settings.DATA_RSID` as an aggregation field name rather than a query and is unaffected; integration tests need a live ES and are not required for this step.

- [ ] **Step 7: Verify against the live local index**

Requires the local ES from `annoq-database` running with index `annoq-annotations-tm-20260828` loaded. All four inputs must return the **same non-zero** count, and the HRC clause must still exclude non-HRC variants:

```bash
IDX=annoq-annotations-tm-20260828
for RS in rs1632919 RS1632919 Rs1632919 "  rs1632919  "; do
  NORM=$(echo "$RS" | tr -d ' ' | tr 'A-Z' 'a-z')
  n=$(curl -s "localhost:9200/$IDX/_search" -H 'Content-Type: application/json' -d "{
    \"size\":0,\"track_total_hits\":true,
    \"query\":{\"bool\":{\"filter\":[{\"term\":{\"rs_dbSNP.keyword\":\"$NORM\"}},{\"term\":{\"Mapped_in_HRC.keyword\":\"Y\"}}]}}}" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['hits']['total']['value'])")
  printf "  input '%s' -> '%s' -> %s hits\n" "$RS" "$NORM" "$n"
done
```

Expected: `1 hits` for all four. Then confirm the subset clause has not regressed — an `N`-mapped rsID must return 0 under it:

```bash
curl -s "localhost:9200/$IDX/_search" -H 'Content-Type: application/json' -d '{
 "size":0,"track_total_hits":true,
 "query":{"bool":{"filter":[{"term":{"rs_dbSNP.keyword":"rs1768385286"}},{"term":{"Mapped_in_HRC.keyword":"Y"}}]}}}' \
 | python3 -c "import json,sys;print('N-mapped rsID under HRC filter:',json.load(sys.stdin)['hits']['total']['value'],'(must be 0)')"
```

- [ ] **Step 8: Commit**

```bash
git add src/graphql/resolvers/helper_resolver.py test/unit/test_query_builders_hrc.py
git commit -m "For #78 Normalize rsID search input and match rs_dbSNP.keyword

rs_dbSNP is a text field, so an un-analyzed term query against the bare field
was case-sensitive: RS1632919 and whitespace-padded input silently returned
zero hits on both the HRC and non-HRC paths. Strip and lower-case the input and
match the exact .keyword sub-field instead."
```

---

### Task 2: Documentation — env warning and stale-spec corrections

**Files:**
- Modify: `.env-example` (the only tracked env file; `.env` and `.env-topmed` are gitignored)
- Modify: `docs/superpowers/specs/2026-07-15-hrc-search-design.md` (lines 25, 50, 51, 98, 125, 137 + header note)

**Interfaces:**
- Consumes: the `_rsid_field()` / `.keyword` convention established in Task 1.
- Produces: no code API. Documentation only.

- [ ] **Step 1: Document the two incompatible uses of `DATA_RSID_COL`**

In `.env-example`, replace this line:

```
DATA_RSID_COL = "rs_dbSNP"
```

with:

```
# Elasticsearch field holding the dbSNP rsID.
# This value is used in TWO ways that are NOT interchangeable:
#   1. QUERY field  - src/graphql/resolvers/helper_resolver.py appends ".keyword" for rsID
#      lookups. rs_dbSNP is a `text` field, so an un-analyzed term query against the bare
#      field is case-sensitive and silently returns 0 hits for input like "RS123".
#   2. _source PROJECTION - src/routers/snp_router_helpers.py DEFAULT_SEARCH_PARAM.
#      Do NOT append ".keyword" there: sub-fields are absent from _source, so the field
#      would silently disappear from responses.
# If you change this field name, check both call sites.
DATA_RSID_COL = "rs_dbSNP"
```

Leave the commented `#DATA_RSID_COL = "rs_dbSNP151"` line directly below it untouched.

- [ ] **Step 2: Verify the env change is syntactically inert**

```bash
grep -c "^DATA_RSID_COL" .env-example
python3 -c "
for ln in open('.env-example'):
    s=ln.strip()
    if s and not s.startswith('#'):
        assert '=' in s, f'bad line: {s}'
print('.env-example parses: every non-comment line is key=value')
"
```

Expected: `1`, then the parse confirmation. Comment lines start with `#` and are ignored by `python-dotenv`.

- [ ] **Step 3: Correct the six stale `HRC_rs_dbSNP151` references**

In `docs/superpowers/specs/2026-07-15-hrc-search-design.md`:

**Line 25** — delete the whole `HRC_rs_dbSNP151` bullet. That column was removed from `annotation_tree.csv` and does not exist in the index.

**Lines 50–51** — the mode table. Replace:

```
| rsID | `*_by_RsID` | term on `rs_dbSNP` | term on `HRC_rs_dbSNP151` + `Mapped_in_HRC=Y` |
| rsID List | `*_by_RsIDs` | terms on `rs_dbSNP` | terms on `HRC_rs_dbSNP151` + `Mapped_in_HRC=Y` |
```

with:

```
| rsID | `*_by_RsID` | term on `rs_dbSNP.keyword` | term on `rs_dbSNP.keyword` + `Mapped_in_HRC=Y` |
| rsID List | `*_by_RsIDs` | terms on `rs_dbSNP.keyword` | terms on `rs_dbSNP.keyword` + `Mapped_in_HRC=Y` |
```

**Line 98** — replace:

```
- **`rsID_query` / `rsIDs_query`** — when `search_hrc`, term/terms on `HRC_rs_dbSNP151`
  (mirroring how `settings.DATA_RSID` is queried today) instead of `settings.DATA_RSID`.
```

with:

```
- **`rsID_query` / `rsIDs_query`** — term/terms on `rs_dbSNP.keyword` (input stripped and
  lower-cased), plus the subset clause when `search_hrc`. The HRC rsID column was dropped,
  so both modes query the same field and differ only by the subset clause.
```

**Line 125** — replace `⇒ target `HRC_rs_dbSNP151` + subset clause.` with `⇒ target `rs_dbSNP.keyword` + subset clause.`

**Line 137** — remove `HRC_rs_dbSNP151` from the list of result fields, leaving `Mapped_in_HRC`.

- [ ] **Step 4: Add the header note and fix the supersession claim**

In the same file, replace these two header lines:

```
Supersedes the mechanism sketched in [`docs/issue-78-hrc-mapping.md`](../../issue-78-hrc-mapping.md)
(that doc proposed carrying the flag on `FilterArgs` with an OR clause; this design does neither).
```

with:

```
> **Status:** records the *original design intent* (2026-07-15). Two things changed after it was
> written: the `HRC_rs_dbSNP151` column was dropped from the index, so HRC rsID search uses
> `rs_dbSNP` restricted by `Mapped_in_HRC=Y`; and rsID queries now target the `.keyword`
> sub-field with normalized input (see
> [`2026-08-31-rsid-case-normalization-design.md`](2026-08-31-rsid-case-normalization-design.md)).
> For the **as-built** contract, read
> [`docs/issue-78-hrc-mapping.md`](../../issue-78-hrc-mapping.md), which was rewritten on
> 2026-08-03 and is authoritative.
```

- [ ] **Step 5: Verify no stale references remain**

```bash
grep -rn "HRC_rs_dbSNP151" docs/ || echo "none in docs/"
grep -rn "HRC_rs_dbSNP151" src/ test/ --exclude-dir=generated || echo "none in src/ or test/ (excluding generated build artifacts)"
```

Expected: both "none" messages.

`--exclude-dir=generated` is required, not cosmetic: `src/graphql/models/generated/snp.py` and
`snp_aggs.py` still declare `HRC_rs_dbSNP151` on disk. They are **gitignored build artifacts** left
over from a pre-rebuild generation, and are corrected by regenerating against the new index (see
Post-implementation), not by this task. Without the exclusion this check reports a false failure.

- [ ] **Step 6: Commit**

```bash
git add .env-example docs/superpowers/specs/2026-07-15-hrc-search-design.md
git commit -m "For #78 Document DATA_RSID_COL dual use; correct stale HRC rsID design

.env-example now records that DATA_RSID_COL is used both as a query field
(where .keyword is appended) and as a _source projection name (where it must
not be). The 2026-07-15 design still described HRC rsID search against the
since-removed HRC_rs_dbSNP151 column; corrected to rs_dbSNP.keyword and marked
as original-intent with a pointer to the as-built doc."
```

---

## Post-implementation

Two items from `CLAUDE.md`'s working rules, outside this plan's scope:

1. **GraphQL playground check** — run an `*_by_RsID` query with `search_hrc: true` and a mixed-case rsID against the local index, confirming a non-empty result. `CLAUDE.md` requires real-query verification for resolver changes.
2. **Regenerate the models** after re-indexing, per "Still needed after a data rebuild" in `docs/issue-78-hrc-mapping.md` — `scripts/class_generators/generate_model.sh` with `ES_INDEX` pointed at the new index, so `HRC_rs_dbSNP151` drops out and `chr_pos` / `HRC_chr_pos` / `HRC_chr_pos_ref_alt` appear. This is unrelated to the rsID fix but is a prerequisite for the site displaying the HRC fields.

`CLAUDE.md` also calls for running `../annoq-proj` → `/annoq-doc-sync` after changing a shared contract. This change alters query construction, not the API contract — the argument names, field names and response shape are unchanged — so a doc-sync is not required. Worth confirming with the hub if in doubt.
