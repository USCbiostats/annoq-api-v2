# Issue #78 — HRC-mapping search (api-v2, as built)

Owning issue: [annoq-site#78](https://github.com/USCbiostats/annoq-site/issues/78). This documents
the **implemented** HRC-search contract in api-v2 (branch `annoq-site-78-add-hrc-mapping-info`).
The data side (data-builder → index) produces the HRC columns; api-v2 exposes a `search_hrc` flag
that restricts results to the HRC-mapped subset in hg19 coordinate space.

## HRC columns in the index

Produced by `annoq-data-builder/wgsa_add/merge_hrc_topmed.py` (TOPMed-only, SNPs only) and
registered in `annoq-site/metadata/annotation_tree.csv`:

- **`Mapped_in_HRC`** — `Y` (hg19-equivalent SNP found in HRC r1.1) / `N` (not found) /
  `.` (`ref_hg19 != ref_hg38`).
- **`HRC_chr_pos`** — hg19 `chr:pos` when `Mapped_in_HRC=Y`, else empty.
- **`HRC_chr_pos_ref_alt`** — hg19 `chr:posREF>ALT` (e.g. `18:10005A>T`) when `Y`, else empty.
- **`chr_pos`** — hg38 `chr:pos`, always populated (basic info).

The HRC rsID is **not** carried — the raw HRC ID column never provides an rsID that TOPMed's own
`rs_dbSNP` lacks (verified on chr18), so HRC-by-RSID search uses `rs_dbSNP` (there is no
`HRC_rs_dbSNP151` field).

## The GraphQL argument

api-v2 runs Strawberry with `auto_camel_case=False` (`src/main.py`), so names are used verbatim.

- **`search_hrc: Boolean`** (Python `Optional[bool] = None`), **default off**. A standalone
  top-level argument on each query field — **not** a field on `filter_args`/`page_args`.
- **Accepted by:** the chromosome, RsID, RsIDs, IDs, and gene_product families — each of
  `get_SNPs_by_*`, `get_aggs_by_*`, `count_SNPs_by_*`, `download_SNPs_by_*` — plus `gene_info`.
  **Not** the `*_by_keyword` family or `annotations`.

## Behavior when `search_hrc: true`

All HRC-mode queries append the subset clause `{"term": {"Mapped_in_HRC.keyword": "Y"}}`
(`hrc.mapped_in_hrc_clause()`), and the coordinate basis flips to **hg19**:

| Search | HRC-mode match |
|--------|----------------|
| Chromosome | range on `chr_hg19` / `pos_hg19` |
| Gene product | PANTHER → **hg19** location dict → chromosome range on `chr_hg19`/`pos_hg19` |
| rsID / rsIDs | `rs_dbSNP` (same as normal) + `Mapped_in_HRC=Y` |
| IDs (VCF file) | `terms` on `HRC_chr_pos_ref_alt.keyword` (hg19 `chr:posREF>ALT`) + `Mapped_in_HRC=Y` |

Response shape is unchanged — the flag only changes *which documents match*. To display hg19/HRC
data, explicitly select the (already-existing) SNP fields: `Mapped_in_HRC`, `HRC_chr_pos`,
`HRC_chr_pos_ref_alt`, `chr_pos`, `chr_hg19`, `pos_hg19`, `ref_hg19`, `alt_hg19`.

## Where it lives (implemented)

- **`src/graphql/resolvers/hrc.py`** — field-name constants (`MAPPED_IN_HRC_FIELD`,
  `HRC_ID_FIELD = "HRC_chr_pos_ref_alt"`, `HG19_CHR_FIELD`, `HG19_POS_FIELD`) and
  `mapped_in_hrc_clause()`.
- **`src/graphql/resolvers/helper_resolver.py`** — `chromosome_query`, `rsID_query`, `rsIDs_query`,
  `IDs_query` branch on `search_hrc`; `gene_query` picks the hg19 location dict.
- **`src/graphql/gene_pos.py`** — `chromosomal_location_dic_hg19` loaded from
  `data/others/Homo_sapiens.chromosome_location_hg19`.
- **REST parity:** `?search_hrc=true` on `/snp/chr`, `/snp/rsidList`, `/snp/gene_product` and their
  `/count/*` and `/download` variants (`src/routers/snp.py`, `snp_router_helpers.py`, `streaming.py`).
  No REST IDs/keyword endpoint.
- **Tests:** `test/unit/test_hrc.py`, `test_query_builders_hrc.py`, `test_gene_hrc.py`,
  `test_api_rest_hrc.py` (all passing).

## Example GraphQL (chromosome search, HRC on)

```graphql
query ChrHRC($chr: String!, $start: Int!, $end: Int!, $hrc: Boolean) {
  get_SNPs_by_chromosome(
    chr: $chr, start: $start, end: $end,
    query_type_option: SNPS,
    page_args: { from: 0, size: 50 },
    search_hrc: $hrc
  ) {
    snps { id chr pos chr_hg19 pos_hg19 Mapped_in_HRC HRC_chr_pos HRC_chr_pos_ref_alt }
  }
}
```
Variables: `{ "chr": "18", "start": 100, "end": 200, "hrc": true }`.

## Still needed after a data rebuild

The generated GraphQL models (`src/graphql/models/generated/snp.py`, `snp_aggs.py`) are built from
the live ES schema. After re-indexing with the new columns, **regenerate them**
(`scripts/class_generators/generator.py`) so `HRC_rs_dbSNP151` drops out and `HRC_chr_pos` /
`HRC_chr_pos_ref_alt` / `chr_pos` appear. Also refresh `data/anno_tree.json` +
`data/api_mapping_anno_tree.json` from the updated `annotation_tree.csv`.
