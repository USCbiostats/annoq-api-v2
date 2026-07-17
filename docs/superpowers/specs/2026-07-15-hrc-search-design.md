# Design — HRC-subset search parameter (Issue #78)

Date: 2026-07-15
Branch: `annoq-site-78-add-hrc-mapping-info`
Owning issue: [annoq-site#78](https://github.com/USCbiostats/annoq-site/issues/78)
Supersedes the mechanism sketched in [`docs/issue-78-hrc-mapping.md`](../../issue-78-hrc-mapping.md)
(that doc proposed carrying the flag on `FilterArgs` with an OR clause; this design does neither).

## Goal

Let a search restrict results to the **HRC subset** of the TOPMed dataset. HRC is a subset of
hg19: when the user opts in (a "Search HRC data" checkbox on the site), the search is performed in
hg19 coordinate/identifier space and restricted to records with `Mapped_in_HRC = Y`. When the user
does **not** opt in, every query behaves exactly as it does today.

This is a TOPMed-stack feature. Docs/SNPWay/annoq-py/AnnoQR are a later step.

## The two new ES fields (already in the index)

Registered in `annoq-site/metadata/annotation_tree.csv` under **HG19 Info**; present in `data/anno_tree.json`.

- **`Mapped_in_HRC`** (`field_type: text`) — always populated: `Y` (hg19-equivalent variant found in
  HRC r1.1), `N` (not found), or `.` (no hg19 mapping). Because it is a text field and the value is
  uppercase, term queries use **`Mapped_in_HRC.keyword`** with value `"Y"`.
- **`HRC_rs_dbSNP151`** (`field_type: text`) — the HRC `rs_dbSNP151` id when `Mapped_in_HRC = Y`,
  else empty string.

Related hg19 fields already present and used by this feature:
`chr_hg19` (text), `pos_hg19` (**long**), `ref_hg19` (text), `alt_hg19` (text).

## Mechanism

A new explicit GraphQL argument **`search_hrc: Optional[bool] = None`** is added to each affected
query field and threaded down to the query builders. It is **not** carried on `FilterArgs`.
Absent / `None` / `False` ⇒ unchanged behavior.

HRC specifics (field names, the `Mapped_in_HRC` clause, the VCF variant-ID parser) are centralized in
a new module **`src/graphql/resolvers/hrc.py`** so the field names live in one place and the parser is
unit-testable. The four query builders call the helper and branch on the flag.

## Site → API mapping (the consumer)

From `annoq-site` (`src/app/main/apps/snp/services/snp.service.ts`), the active search modes map to:

| Site search mode | API request family | Normal (hg38) query | HRC-mode query |
|---|---|---|---|
| Chromosome | `*_by_chromosome` | range on `chr` + `pos` | range on `chr_hg19` + `pos_hg19` + `Mapped_in_HRC=Y` |
| VCF File (`chromosomeList`) | `*_by_IDs` | match `_id` (`chr:pos ref>alt`, hg38) | per-variant match on `chr_hg19`+`pos_hg19`+`ref_hg19`+`alt_hg19` + `Mapped_in_HRC=Y` (Option B) |
| Gene Product | `gene_info` then `*_by_gene_product` | PANTHER → hg38 dict → range on `chr`+`pos` | PANTHER → hg19 dict → range on `chr_hg19`+`pos_hg19` + `Mapped_in_HRC=Y` |
| rsID | `*_by_RsID` | term on `rs_dbSNP` | term on `HRC_rs_dbSNP151` + `Mapped_in_HRC=Y` |
| rsID List | `*_by_RsIDs` | terms on `rs_dbSNP` | terms on `HRC_rs_dbSNP151` + `Mapped_in_HRC=Y` |

Keyword and Gene Id modes are commented out on the site — out of scope. The site's checkbox/param
wiring is not yet implemented; this API defines the contract the site will introspect.

## Affected layers

| Layer | File | Change |
|---|---|---|
| GraphQL fields | `src/graphql/schema.py` | add `search_hrc` arg to the 4 families × {get, aggs, count, download} (20 fields) and to `gene_info`; pass down |
| SNP resolvers | `src/graphql/resolvers/snp_resolver.py` | add `search_hrc` param to `search_by_chromosome/rsID/rsIDs/IDs/gene`; pass to builders and streaming |
| Count resolvers | `src/graphql/resolvers/count_resolver.py` | add `search_hrc` to `count_by_chromosome/rsID/rsIDs/IDs/gene`; pass to builders |
| Download stream | `src/graphql/resolvers/large_result_streaming_resolver.py` | add `search_hrc` to `stream_by_chromosome/rsIDs/IDs/gene_product`; pass to builders |
| Query builders | `src/graphql/resolvers/helper_resolver.py` | branch `chromosome_query`, `rsID_query`, `rsIDs_query`, `IDs_query`, `gene_query` on `search_hrc` |
| Gene coords | `src/graphql/gene_pos.py` | load a second module-level dict from `data/others/Homo_sapiens.chromosome_location_hg19` |
| New helper | `src/graphql/resolvers/hrc.py` | field map, `Mapped_in_HRC` clause builder, variant-ID parser |

`*_by_keyword` requests are untouched (no coordinate/rsID/subset semantics).

### REST layer (the Swagger `/docs` surface)

The GraphQL router is mounted with `include_in_schema=False`, so it never appears in Swagger.
The Swagger surface is the **REST** router (`src/routers/snp.py`), which mirrors search/count/download
and calls its own resolvers. These call the same query builders, so `search_hrc` threads the same way:

| Layer | File | Change |
|---|---|---|
| REST endpoints | `src/routers/snp.py` | `search_hrc` on `/snp/chr`, `/snp/rsidList`, `/snp/gene_product` and the three `/count/*` |
| Download endpoints | `src/routers/streaming.py` | `search_hrc` on the three `/*/download` routes, threaded through `create_streaming_response` |
| Shared query params | `src/routers/snp_router_helpers.py` | `search_hrc: bool = False` on `CommonSearchQueryParams` and `StreamingQueryParams` |
| REST search resolver | `src/graphql/resolvers/api_snp_resolver.py` | `search_hrc` on `search_by_chromosome`/`search_by_rsIDs`/`search_by_gene_product` |
| REST count resolver | `src/graphql/resolvers/api_count_resolver.py` | `search_hrc` on `count_by_chromosome`/`count_by_rsIDs`/`count_by_gene_product` |

REST has no VCF/IDs endpoint, so Option B does not apply there. REST exposes the flag as a plain
`bool` (default `false`) for a clean Swagger control; GraphQL uses `Optional[bool] = None`.

## Query-builder behavior (HRC mode; else unchanged)

All HRC-mode branches append the subset clause `{"term": {"Mapped_in_HRC.keyword": "Y"}}` to
`query["bool"]["filter"]`, plus:

- **`chromosome_query(chr, start, end, filter_args, search_hrc)`** — when `search_hrc`, match
  `{"term": {"chr_hg19": chr}}` (mirroring how `chr` is queried today; verify `.keyword` need against
  live mapping) and `{"range": {"pos_hg19": {"gte": start, "lte": end}}}` (numeric; `pos_hg19` is `long`).
- **`gene_query(gene, filter_args, search_hrc)`** — when `search_hrc`, resolve coords from the hg19
  dict (`chromosomal_location_dic_hg19`) and delegate to `chromosome_query(..., search_hrc=True)` so it
  inherits the hg19 field switch and subset clause.
- **`rsID_query` / `rsIDs_query`** — when `search_hrc`, term/terms on `HRC_rs_dbSNP151`
  (mirroring how `settings.DATA_RSID` is queried today) instead of `settings.DATA_RSID`.
- **`IDs_query(ids, filter_args, search_hrc)` — Option B** — when `search_hrc`, parse each id of the
  form `chr:pos ref>alt` (e.g. `18:12345A>G`) into `(chr, pos, ref, alt)` and build a
  `bool.should` (`minimum_should_match: 1`) where each variant is a `bool.must` of exact matches on
  `chr_hg19`, `pos_hg19`, `ref_hg19`, `alt_hg19`. This preserves the current exact-variant semantics of
  the `_id` lookup, but in hg19 space. Ids that fail to parse are skipped.

`gene_info` (`schema.py`) gains `search_hrc`; when set it returns hg19 coords (from the hg19 dict) so
the site's displayed gene location matches the hg19 results.

## Decisions

1. **Parameter is explicit, not `FilterArgs`.** Per the requirement; each affected field takes its own
   `search_hrc: Optional[bool] = None`.
2. **`gene_info` gets the flag** and returns hg19 coords in HRC mode (display consistency with results).
3. **VCF Option B matches all four hg19 fields** (chr+pos+ref+alt), an exact-variant match equivalent
   to today's `_id` lookup — not chr+pos only.
4. **`Mapped_in_HRC` term uses `.keyword`** with value `"Y"`.

## Testing

`pytest` coverage (mirror existing resolver/query-builder tests):

- Each builder, `search_hrc=None` ⇒ identical to current output (regression).
- `chromosome_query` with `search_hrc=True` ⇒ uses `chr_hg19`/`pos_hg19` and appends the
  `Mapped_in_HRC.keyword=Y` clause.
- `rsID_query`/`rsIDs_query` with `search_hrc=True` ⇒ target `HRC_rs_dbSNP151` + subset clause.
- `IDs_query` with `search_hrc=True` ⇒ correct `bool.should` per-variant structure; variant-ID parser
  unit tests (valid ids, multi-base indels, malformed ids skipped).
- `gene_query`/`gene_info` with `search_hrc=True` ⇒ hg19 coord dict is used.
- Integration: real queries in the GraphQL playground against the local HRC test index
  (`annoq-annotations-tm-hrc-test-20260709`): `search_hrc=true` returns only HRC-mapped records; gene
  search returns hg19 coords.

## Out of scope / follow-ups

- Regenerating GraphQL models (`snp.py`/`snp_aggs.py`) is only needed if the two HRC fields must be
  *returned/selectable*; this feature only *filters* on them. Regenerate if the site needs to display
  `Mapped_in_HRC` / `HRC_rs_dbSNP151` in results.
- Site checkbox wiring (`annoq-site`), and downstream docs (`../annoq-proj` → `/annoq-doc-sync`).
