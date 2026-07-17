"""Unit tests for the HRC-subset search helper (src/graphql/resolvers/hrc.py).

These are pure-function tests (no Elasticsearch). The exact term syntax asserted
here was verified empirically against the local HRC test index
(annoq-annotations-tm-hrc-test-20260709): text fields require the `.keyword`
sub-field for exact matches, `pos_hg19` is a numeric `long`.
"""

from src.graphql.resolvers import hrc


def test_mapped_in_hrc_clause_uses_keyword_subfield():
    # Mapped_in_HRC is a text field storing uppercase "Y"; bare term would miss it.
    assert hrc.mapped_in_hrc_clause() == {"term": {"Mapped_in_HRC.keyword": "Y"}}


def test_parse_variant_id_snp():
    assert hrc.parse_variant_id("18:14175A>T") == ("18", 14175, "A", "T")


def test_parse_variant_id_strips_whitespace():
    assert hrc.parse_variant_id("  18:14175A>T  ") == ("18", 14175, "A", "T")


def test_parse_variant_id_multibase_indel():
    assert hrc.parse_variant_id("2:100AC>GTT") == ("2", 100, "AC", "GTT")


def test_parse_variant_id_non_numeric_chromosome():
    assert hrc.parse_variant_id("X:500G>A") == ("X", 500, "G", "A")


def test_parse_variant_id_malformed_returns_none():
    assert hrc.parse_variant_id("not-a-variant") is None
    assert hrc.parse_variant_id("18:14175A") is None  # no alt
    assert hrc.parse_variant_id("18:posA>T") is None  # non-numeric pos
    assert hrc.parse_variant_id("") is None
    assert hrc.parse_variant_id(None) is None


def test_hrc_variant_clause_exact_match_on_hg19_fields():
    # ref/alt must use .keyword (uppercase bases don't match the analyzed text field).
    assert hrc.hrc_variant_clause("18:14175A>T") == {
        "bool": {
            "must": [
                {"term": {"chr_hg19.keyword": "18"}},
                {"term": {"pos_hg19": 14175}},
                {"term": {"ref_hg19.keyword": "A"}},
                {"term": {"alt_hg19.keyword": "T"}},
            ]
        }
    }


def test_hrc_variant_clause_malformed_returns_none():
    assert hrc.hrc_variant_clause("garbage") is None
