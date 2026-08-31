# Design — rsID search normalization (case + whitespace)

Date: 2026-08-31
Branch: `annoq-site-78-add-hrc-mapping-info`
Owning issue: [annoq-site#78](https://github.com/USCbiostats/annoq-site/issues/78)

Related docs:
- [`docs/issue-78-hrc-mapping.md`](../../issue-78-hrc-mapping.md) — the **as-built** HRC-search
  contract. Authoritative for HRC behavior; this design does not change it.
- [`docs/superpowers/specs/2026-07-15-hrc-search-design.md`](2026-07-15-hrc-search-design.md) —
  the original HRC design, now partly stale. Correcting it is in scope here (§6).

---

## 1. Problem

rsID search silently returns **zero results** when the user's input differs from the stored value
by case or surrounding whitespace. There is no error — the query simply matches nothing.

Verified against the live local index `annoq-annotations-tm-20260828` (50,000 chr6 docs), using a
real HRC-mapped rsID (`rs1632919`):

| input | `term` on `rs_dbSNP` | `term` on `rs_dbSNP.keyword` |
|---|---|---|
| `rs1632919` | 1 | 1 |
| `RS1632919` | **0** | **0** |
| `Rs1632919` | **0** | **0** |
| `' rs1632919'` (leading space) | — | **0** |
| `'rs1632919 '` (trailing space) | — | **0** |

This affects **both** the HRC and non-HRC rsID paths, and both the single (`rsID`) and list
(`rsIDs`) families, across GraphQL and REST.

## 2. Root cause

`rs_dbSNP` is mapped as `text` with a `.keyword` sub-field:

```json
{"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 10000}}}
```

A `term` query is **not analyzed**. Against the analyzed `text` field it looks for the literal
token, and the standard analyzer has already lower-cased what was indexed — so `RS1632919` finds
nothing. Against `.keyword` it must match the raw value byte-for-byte, so both case and stray
whitespace fail.

The current code works only because dbSNP rsIDs are conventionally lower-case `rs` + digits, which
happens to survive the analyzer as a single identical token. It is correct by coincidence, not by
construction.

The same reasoning was already applied correctly elsewhere in this codebase: the
2026-07-15 design notes that because `Mapped_in_HRC`'s value `Y` is uppercase, its term query must
target `Mapped_in_HRC.keyword`. That reasoning was simply never carried across to `rs_dbSNP`.

## 3. Scope

**In scope**

- Normalize rsID input (lower-case + strip surrounding whitespace) and match against
  `rs_dbSNP.keyword`, at all four query sites.
- Update the three existing unit assertions that encode the current query shape.
- Add coverage for mixed-case and whitespace-padded input.
- Correct the stale `HRC_rs_dbSNP151` references in the 2026-07-15 design (§6).

**Out of scope — already built or already documented**

- The `search_hrc` feature itself: implemented, tested, and documented in
  `docs/issue-78-hrc-mapping.md`. Verified working against the new index — an `N`-mapped rsID
  returns 1 hit unfiltered and 0 with the `Mapped_in_HRC=Y` clause.
- Regenerating `src/graphql/models/generated/` after the data rebuild. Those files are
  **gitignored build artifacts**; the requirement is already recorded under "Still needed after a
  data rebuild" in `docs/issue-78-hrc-mapping.md`, and `data/anno_tree.json` /
  `data/api_mapping_anno_tree.json` were refreshed on 2026-08-25.
- Any change to hg19 coordinate handling, the HRC subset clause, or response shape.

## 4. Design

Add two small module-level helpers in `src/graphql/resolvers/helper_resolver.py`, beside the query
builders that use them:

```python
def _rsid_field() -> str:
    """Exact-match sub-field for rsID lookups.

    rs_dbSNP is a `text` field, so a term query against it is analyzed and therefore
    case-sensitive in practice. Match the raw value via `.keyword` instead, and normalize
    the caller's input to suit (see _normalize_rsid).
    """
    return f"{settings.DATA_RSID}.keyword"


def _normalize_rsid(rsID: str) -> str:
    """Normalize user-supplied rsID input for exact `.keyword` matching.

    dbSNP rsIDs are stored lower-case with no surrounding whitespace. Users paste them from
    papers and spreadsheets, which commonly introduces upper-case ("RS1632919") or padding.
    Both return zero hits against `.keyword` without this.
    """
    return rsID.strip().lower()
```

Both the single and list builders use them:

```python
{"term":  {_rsid_field(): _normalize_rsid(rsID)}}
{"terms": {_rsid_field(): [_normalize_rsid(r) for r in rsIDs]}}
```

**Why `.keyword` + normalization rather than `match`.** A `match` query on the `text` field is
case-insensitive for free, but it is analyzed: were `rs_dbSNP` ever to become multi-valued, `match`
would silently begin matching *any* token in the field, changing search semantics without any code
change. `.keyword` is exact and fails loudly instead. This is safe here because `rs_dbSNP` holds a
single rsID — a wildcard scan for `;`, `|` and `,` across all 50,000 indexed docs found **zero**
delimiters.

**Behavior change beyond the defect.** Normalization applies to the non-HRC path too, so ordinary
rsID search also becomes case- and whitespace-insensitive. That is the intended improvement, not a
side effect, but it is user-visible and worth noting in release notes.

## 5. Where

`src/graphql/resolvers/helper_resolver.py` — four query sites:

| Line | Function | Branch |
|---|---|---|
| 211 | `rsID_query` | `search_hrc` |
| 220 | `rsID_query` | normal |
| 250 | `rsIDs_query` | `search_hrc` |
| 256 | `rsIDs_query` | normal |

**Do not change** `src/routers/snp_router_helpers.py:12`. It uses `settings.DATA_RSID` to build a
`_source` projection list, not a query; `.keyword` there would request a sub-field that is not
stored in `_source` and would drop the field from responses.

`src/config/settings.py` and `src/graphql/resolvers/hrc.py` are unchanged — this is not
HRC-specific, so it does not belong in `hrc.py`.

## 6. Correcting the 2026-07-15 design

That spec predates the removal of the `HRC_rs_dbSNP151` column and still describes HRC rsID search
as targeting it. Six references, at lines **25, 50, 51, 98, 125, 137**. The as-built behavior is
`rs_dbSNP` + `Mapped_in_HRC=Y`.

Corrections:

- **Line 25** — remove the `HRC_rs_dbSNP151` column entry; the column does not exist in the index.
- **Lines 50–51** (mode table) — HRC-mode rsID / rsID-List become
  `term`/`terms` on `rs_dbSNP.keyword` + `Mapped_in_HRC=Y`.
- **Line 98** — `rsID_query` / `rsIDs_query` target `rs_dbSNP.keyword`, not `HRC_rs_dbSNP151`.
- **Line 125** (acceptance criteria) — same substitution.
- **Line 137** — drop `HRC_rs_dbSNP151` from the list of result fields.

Add a note near the top recording that the HRC rsID mechanism changed after this design was
written, with a pointer to `docs/issue-78-hrc-mapping.md` as the authoritative as-built contract.

The header's supersession claim also needs attention: it states this design *supersedes*
`docs/issue-78-hrc-mapping.md`, but that document was rewritten on 2026-08-03 to describe the
as-built system and is now the current reference. The relationship should read: this design records
the original intent; `issue-78-hrc-mapping.md` records what was built.

## 7. Verification

**Unit.** Three existing assertions in `test/unit/test_query_builders_hrc.py` (lines 48, 57, 68)
encode the current shape and must be updated to the `.keyword` field. Add cases covering:

| Input | Expected |
|---|---|
| `rs123` | `{"term": {"rs_dbSNP.keyword": "rs123"}}` |
| `RS123` | normalizes to `rs123` |
| `Rs123` | normalizes to `rs123` |
| `" rs123 "` | normalizes to `rs123` |
| `["rs1", "RS2", " Rs3 "]` | `["rs1", "rs2", "rs3"]` |

`test/integration/test_module_query.py:178-179` uses `settings.DATA_RSID` as an aggregation field
name, not a query, and is unaffected.

**Live.** Against `annoq-annotations-tm-20260828`, each of `rs1632919`, `RS1632919`, `Rs1632919`
and `" rs1632919 "` must return the same non-zero hit count, both with and without `search_hrc`.
An `N`-mapped rsID must still return 0 hits under `search_hrc` — that clause must not regress.

Per `CLAUDE.md`, resolver/query changes need `pytest` coverage and verification of real queries in
the GraphQL playground.

## 8. Files touched

```
src/graphql/resolvers/helper_resolver.py                    (+2 helpers, 4 call sites)
test/unit/test_query_builders_hrc.py                        (3 assertions updated, ~5 cases added)
docs/superpowers/specs/2026-07-15-hrc-search-design.md      (6 stale refs + header note)
```

No change to generated models, ES mappings, the index, or response shape.
