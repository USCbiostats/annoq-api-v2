"""Unit tests for the HRC-subset search helper (src/graphql/resolvers/hrc.py).

Pure-function / constant tests (no Elasticsearch). The term syntax asserted here was
verified against the local HRC test index (annoq-annotations-tm-hrc-test-20260709):
text fields require the `.keyword` sub-field for exact matches, `pos_hg19` is numeric.
"""

from src.graphql.resolvers import hrc


def test_mapped_in_hrc_clause_uses_keyword_subfield():
    # Mapped_in_HRC is a text field storing uppercase "Y"; a bare term would miss it.
    assert hrc.mapped_in_hrc_clause() == {"term": {"Mapped_in_HRC.keyword": "Y"}}


def test_hrc_field_names():
    # HRC-mode ES field names used by the query builders.
    assert hrc.MAPPED_IN_HRC_FIELD == "Mapped_in_HRC"
    assert hrc.HRC_ID_FIELD == "HRC_chr_pos_ref_alt"
    assert hrc.HG19_CHR_FIELD == "chr_hg19"
    assert hrc.HG19_POS_FIELD == "pos_hg19"
