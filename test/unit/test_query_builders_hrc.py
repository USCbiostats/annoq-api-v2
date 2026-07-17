"""Unit tests for the search_hrc branch of the ES query builders.

Pure-function tests over the query dicts (no Elasticsearch). Without the flag the
builders must produce byte-for-byte the same query as before (regression); with
the flag they switch to hg19 fields / HRC_rs_dbSNP151 and append Mapped_in_HRC=Y.
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


def test_rsID_query_with_hrc_uses_hrc_rsid_field_and_subset_clause():
    assert rsID_query("rs123", search_hrc=True) == {
        "bool": {
            "filter": [
                {"term": {"HRC_rs_dbSNP151.keyword": "rs123"}},
                MAPPED,
            ]
        }
    }


def test_rsIDs_query_with_hrc_uses_hrc_rsid_field():
    assert rsIDs_query(["rs1", "rs2"], search_hrc=True) == {
        "bool": {
            "filter": [
                {"terms": {"HRC_rs_dbSNP151.keyword": ["rs1", "rs2"]}},
                MAPPED,
            ]
        }
    }


# --- IDs (VCF, Option B) ---------------------------------------------------
def test_IDs_query_without_hrc_matches_document_ids():
    assert IDs_query(["18:14175A>T"]) == {
        "bool": {"filter": [{"ids": {"values": ["18:14175A>T"]}}]}
    }


def test_IDs_query_with_hrc_builds_per_variant_positional_should():
    assert IDs_query(["18:14175A>T", "2:100AC>GTT"], search_hrc=True) == {
        "bool": {
            "filter": [
                {
                    "bool": {
                        "should": [
                            {
                                "bool": {
                                    "must": [
                                        {"term": {"chr_hg19.keyword": "18"}},
                                        {"term": {"pos_hg19": 14175}},
                                        {"term": {"ref_hg19.keyword": "A"}},
                                        {"term": {"alt_hg19.keyword": "T"}},
                                    ]
                                }
                            },
                            {
                                "bool": {
                                    "must": [
                                        {"term": {"chr_hg19.keyword": "2"}},
                                        {"term": {"pos_hg19": 100}},
                                        {"term": {"ref_hg19.keyword": "AC"}},
                                        {"term": {"alt_hg19.keyword": "GTT"}},
                                    ]
                                }
                            },
                        ],
                        "minimum_should_match": 1,
                    }
                },
                MAPPED,
            ]
        }
    }


def test_IDs_query_with_hrc_skips_malformed_ids():
    query = IDs_query(["garbage", "18:14175A>T"], search_hrc=True)
    should = query["bool"]["filter"][0]["bool"]["should"]
    assert len(should) == 1
    assert should[0]["bool"]["must"][0] == {"term": {"chr_hg19.keyword": "18"}}
