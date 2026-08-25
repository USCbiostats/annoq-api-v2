"""HRC-subset search helpers.

Centralizes everything specific to the "search HRC data" option (Issue #78):
the hg19 Elasticsearch field names and the ``Mapped_in_HRC`` restriction clause.

Field-name / term-syntax notes (verified against the HRC test index):

- ``Mapped_in_HRC`` and ``HRC_chr_pos_ref_alt`` are text fields; ``chr_hg19`` is a
  text field; ``pos_hg19`` is a numeric ``long``.
- Text fields are analyzed (lower-cased), so exact term matches on case-sensitive
  values (``Y``, a variant id like ``18:10005A>T``) must target the ``.keyword``
  sub-field. ``pos_hg19`` uses a numeric term/range directly.

HRC search semantics (Issue #78) — all HRC-mode queries append ``mapped_in_hrc_clause()``:

- **Chromosome / gene** — range on ``chr_hg19`` / ``pos_hg19`` (hg19 coordinates).
- **rsID** — matched on the normal ``rs_dbSNP`` field (``settings.DATA_RSID``). The raw
  HRC rsID is intentionally NOT carried in the index: it never provides an rsID that
  TopMed's own ``rs_dbSNP`` lacks (verified on chr18), so ``rs_dbSNP`` is used for HRC
  rsID search, restricted to the HRC subset.
- **IDs (VCF file)** — matched on ``HRC_chr_pos_ref_alt`` (hg19 ``chr:posREF>ALT``,
  e.g. ``18:10005A>T``) instead of the hg38 document ``_id``.
"""

# Elasticsearch field names (raw ES names — the query layer uses these directly).
MAPPED_IN_HRC_FIELD = "Mapped_in_HRC"
HRC_ID_FIELD = "HRC_chr_pos_ref_alt"   # hg19 chr:posREF>ALT, e.g. "18:10005A>T"
HG19_CHR_FIELD = "chr_hg19"
HG19_POS_FIELD = "pos_hg19"


def mapped_in_hrc_clause() -> dict:
    """ES filter clause restricting results to HRC-mapped records (Mapped_in_HRC = Y)."""
    return {"term": {f"{MAPPED_IN_HRC_FIELD}.keyword": "Y"}}
