"""Unit tests for the search_hrc branch of the ES query builders.

Pure-function tests over the query dicts (no Elasticsearch). Without the flag the
builders must produce byte-for-byte the same query as before (regression); with the
flag, chromosome/gene switch to hg19 fields, rsID matches the normal `rs_dbSNP`
field, IDs match the hg19 `HRC_chr_pos_ref_alt` field, and every HRC query appends
Mapped_in_HRC=Y.
"""

from src.config.settings import settings
from src.graphql.resolvers.helper_resolver import (
    chromosome_query,
    rsID_query,
    rsIDs_query,
    IDs_query,
)

MAPPED = {"term": {"Mapped_in_HRC.keyword": "Y"}}


# --- chromosome ------------------------------------------------------------
def test_chromosome_query_without_hrc_unchanged():
    assert chromosome_query("18", 100, 200) == {
        "bool": {
            "filter": [
                {"term": {"chr": "18"}},
                {"range": {"pos": {"gte": 100, "lte": 200}}},
            ]
        }
    }


def test_chromosome_query_with_hrc_uses_hg19_fields_and_subset_clause():
    assert chromosome_query("18", 100, 200, search_hrc=True) == {
        "bool": {
            "filter": [
                {"term": {"chr_hg19.keyword": "18"}},
                {"range": {"pos_hg19": {"gte": 100, "lte": 200}}},
                MAPPED,
            ]
        }
    }


# --- rsID / rsIDs ----------------------------------------------------------
def test_rsID_query_without_hrc_uses_primary_rsid_field():
    assert rsID_query("rs123") == {
        "bool": {"filter": [{"term": {settings.DATA_RSID: "rs123"}}]}
    }


def test_rsID_query_with_hrc_uses_primary_rsid_field_and_subset_clause():
    # The raw HRC rsID is not carried; HRC rsID search uses rs_dbSNP + Mapped_in_HRC=Y.
    assert rsID_query("rs123", search_hrc=True) == {
        "bool": {
            "filter": [
                {"term": {settings.DATA_RSID: "rs123"}},
                MAPPED,
            ]
        }
    }


def test_rsIDs_query_with_hrc_uses_primary_rsid_field():
    assert rsIDs_query(["rs1", "rs2"], search_hrc=True) == {
        "bool": {
            "filter": [
                {"terms": {settings.DATA_RSID: ["rs1", "rs2"]}},
                MAPPED,
            ]
        }
    }


# --- IDs (VCF file) --------------------------------------------------------
def test_IDs_query_without_hrc_matches_document_ids():
    assert IDs_query(["18:14175A>T"]) == {
        "bool": {"filter": [{"ids": {"values": ["18:14175A>T"]}}]}
    }


def test_IDs_query_with_hrc_matches_hrc_chr_pos_ref_alt_field():
    # In HRC mode the ids are hg19 chr:posREF>ALT strings matched against the
    # HRC_chr_pos_ref_alt keyword field, restricted to Mapped_in_HRC=Y.
    assert IDs_query(["18:14175A>T", "2:100AC>GTT"], search_hrc=True) == {
        "bool": {
            "filter": [
                {"terms": {"HRC_chr_pos_ref_alt.keyword": ["18:14175A>T", "2:100AC>GTT"]}},
                MAPPED,
            ]
        }
    }
