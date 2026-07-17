# Issue #78 — HRC-mapping search (api-v2 handoff)

Handoff notes carried over from the data/build work done in the sibling repos (owning issue:
[annoq-site#78](https://github.com/USCbiostats/annoq-site/issues/78)). This documents what api-v2
needs to do; the data side (data-builder → database load) is already validated on the local stack.

## Goal

Let the search restrict results to TOPMed SNPs that are **mapped to HRC r1.1**, and return **hg19**
coordinates for HRC-mapped records in gene search. This is a **TOPMed-stack** feature, gated on
coverage (deemed "good enough for now"). Docs/SNPWay/annoq-py/AnnoQR are a later step.

## The two HRC fields (already in the ES index)

Produced by `annoq-data-builder/wgsa_add/merge_hrc_topmed.py` (TOPMed-only), registered in
`annoq-site/metadata/annotation_tree.csv` under **HG19 Info**, and present in the ES mapping.
Exact field names (uppercase — match these exactly):

- **`Mapped_in_HRC`** — `Y` (hg19-equivalent variant found in HRC r1.1) / `N` (not found) /
  `.` (no hg19 mapping, i.e. `ref_hg19 != ref_hg38`).
- **`HRC_rs_dbSNP151`** — the HRC `rs_dbSNP151` id when `Mapped_in_HRC = Y`, else empty string.

Field-name note: the ES field name is the raw column name; api-v2's `_clean_name` (`src/utils.py`)
transforms names for the GraphQL layer (`=`→`_equals_`, strips `()`, etc.). The **ES query builder
uses raw ES field names**; the generated GraphQL model uses the cleaned name.

## Live local dev target

A single-chromosome test index is loaded on the local Docker ES:

- ES: `http://localhost:9200` — index **`annoq-annotations-tm-hrc-test-20260709`**
- 4999 chr18 docs; **109 are `Mapped_in_HRC=Y`** (all 109 also have a non-empty `HRC_rs_dbSNP151`;
  the two sets are identical in this subset). It's a telomeric slice (chr18 pos 10005–45335), so the
  2.18% rate is an unrepresentative floor, not the real coverage.

To develop against it: set `ES_INDEX=annoq-annotations-tm-hrc-test-20260709` and the ES host/URL to
localhost in `.env`, then regenerate models (below) so the two HRC fields appear in the schema.

## Changes to make in api-v2

1. **Accept the parameter.** Add `search_hrc: Optional[bool] = None` to `FilterArgs`
   (`src/graphql/models/annotation_model.py`). `FilterArgs` already flows through every search path,
   so this avoids touching ~20 resolver signatures. Extend `transform_filter_args`
   (`src/graphql/schema.py`) — currently only copies `exists` — to carry the flag.

2. **Add the ES filter clause.** In `src/graphql/resolvers/helper_resolver.py`, the query builders
   (`chromosome_query`, `rsID_query`, `rsIDs_query`, `IDs_query`; `gene_query` reuses
   `chromosome_query`) each build `query["bool"]["filter"]`. When `filter_args.search_hrc` is set,
   append an OR clause — "mapped by hg19 position OR has an HRC rsID":

   ```python
   if filter_args and getattr(filter_args, "search_hrc", None):
       query["bool"]["filter"].append({
           "bool": {"should": [
               {"term":   {"Mapped_in_HRC.keyword": "Y"}},
               {"bool": {"must": [{"exists": {"field": "HRC_rs_dbSNP151"}}],
                         "must_not": [{"term": {"HRC_rs_dbSNP151.keyword": ""}}]}},
           ], "minimum_should_match": 1}
       })
   ```
   (Factor into a small helper and call from each builder.) In the chr18 subset the two conditions
   coincide, but genome-wide a `Y` record can have a blank rsID — the OR is what still catches it.

3. **Gene search → hg19 coordinates.** Gene→coords uses the PantherDB API in
   `src/graphql/gene_pos.py` (`map_gene` → `get_pos_from_gene_id`), and coords come from
   `chromosomal_location_dic`, loaded from `data/others/Homo_sapiens.chromosomal_location_hg_38`.
   Add a second module-level dict loaded from **`data/others/Homo_sapiens.chromosome_location_hg19`**
   (same 5-col TSV format: `gene_accession_key, chr, start, end, strand`; loader reads cols 0–3), and
   select it in `gene_query` (and `schema.py:gene_info`) when the HRC flag is set. `gene_query` is the
   single choke point where `(chr, start, end)` is produced. (The last hg38 commit,
   `Updated for hg38 gene to chromosome location lookup`, introduced exactly this pattern for hg38.)

4. **Regenerate models.** After the index has the two fields, run
   `python3 -m scripts.class_generators.generator` (or `scripts/class_generators/generate_model.sh`)
   → writes `scripts/class_generators/generated_schemas/*.json`, then `datamodel-codegen` builds
   `src/graphql/models/generated/{snp.py,snp_aggs.py}`. Strawberry types wrap them in
   `src/graphql/models/snp_model.py`. Field labels come from `data/anno_tree.json`.

5. **Tests.** Add `pytest` coverage: `search_hrc=true` returns only HRC-mapped records; gene search
   with the flag returns hg19 coords. Verify a real query in the GraphQL playground against the local
   test index.

## Downstream that depends on this

annoq-site regenerates its GraphQL types by introspecting the **live TOPMed api-v2**
(`https://api-v2.topmed.annoq.org/graphql`), so the site's checkbox work needs this deployed there
first (or point the site's codegen at a local api-v2). The site change: remove the `GRCh38/hg38`
label, add a "Search HRC data" checkbox that passes the flag.

## Branch

`annoq-site-78-add-hrc-mapping-info` (this repo). Owning issue is annoq-site#78, so commit messages
here reference it as `For #USCbiostats/annoq-site/issues/78` per the hub's naming convention.
