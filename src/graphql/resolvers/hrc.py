"""HRC-subset search helpers.

Centralizes everything specific to the "search HRC data" option (Issue #78):
the hg19 Elasticsearch field names, the ``Mapped_in_HRC`` restriction clause, and
the VCF variant-id parser used by the IDs query builder.

Field-name / term-syntax notes (verified against the HRC test index
``annoq-annotations-tm-hrc-test-20260709``):

- ``Mapped_in_HRC`` and ``HRC_rs_dbSNP151`` are text fields; ``chr_hg19``,
  ``ref_hg19``, ``alt_hg19`` are text fields; ``pos_hg19`` is a numeric ``long``.
- Text fields are analyzed (lower-cased), so exact term matches on case-sensitive
  values (``Y``, genomic bases like ``A``/``T``) must target the ``.keyword``
  sub-field. ``pos_hg19`` uses a numeric term/range directly.
"""

import re

# Elasticsearch field names (raw ES names — the query layer uses these directly).
MAPPED_IN_HRC_FIELD = "Mapped_in_HRC"
HRC_RSID_FIELD = "HRC_rs_dbSNP151"
HG19_CHR_FIELD = "chr_hg19"
HG19_POS_FIELD = "pos_hg19"
HG19_REF_FIELD = "ref_hg19"
HG19_ALT_FIELD = "alt_hg19"

# Variant id as produced by the site / accepted by the IDs query: "chr:pos ref>alt"
# e.g. "18:14175A>T" or the multi-base indel "2:100AC>GTT".
_VARIANT_ID_RE = re.compile(r"^([^:]+):(\d+)([A-Za-z]+)>([A-Za-z]+)$")


def mapped_in_hrc_clause() -> dict:
    """ES filter clause restricting results to HRC-mapped records (Mapped_in_HRC = Y)."""
    return {"term": {f"{MAPPED_IN_HRC_FIELD}.keyword": "Y"}}


def parse_variant_id(variant_id):
    """Parse a variant id ``chr:pos ref>alt`` into ``(chr, pos:int, ref, alt)``.

    Returns ``None`` if the id is empty/None or does not match the expected shape,
    so malformed ids can be skipped rather than aborting the whole query.
    """
    if not variant_id:
        return None
    match = _VARIANT_ID_RE.match(variant_id.strip())
    if not match:
        return None
    chromosome, pos, ref, alt = match.groups()
    return (chromosome, int(pos), ref, alt)


def hrc_variant_clause(variant_id):
    """Exact-variant match on the hg19 fields for one variant id.

    Mirrors the exact-variant semantics of the normal ``_id`` lookup, but in hg19
    coordinate space. Returns ``None`` if the id cannot be parsed.
    """
    parsed = parse_variant_id(variant_id)
    if parsed is None:
        return None
    chromosome, pos, ref, alt = parsed
    return {
        "bool": {
            "must": [
                {"term": {f"{HG19_CHR_FIELD}.keyword": chromosome}},
                {"term": {HG19_POS_FIELD: pos}},
                {"term": {f"{HG19_REF_FIELD}.keyword": ref}},
                {"term": {f"{HG19_ALT_FIELD}.keyword": alt}},
            ]
        }
    }
