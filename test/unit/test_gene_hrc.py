"""Unit tests for the hg19 gene-location path used by HRC gene search.

Uses a known gene accession present in both location files:
  hg38: chr15 74409289-74433704
  hg19: chr15 74708980-74726001
map_gene (PANTHER network call) is monkeypatched so these tests stay offline.
"""

import src.graphql.resolvers.helper_resolver as helper_resolver
from src.graphql.gene_pos import (
    chromosomal_location_dic,
    chromosomal_location_dic_hg19,
)

GENE_ACCESSION = "HUMAN|HGNC=10741|UniProtKB=O75326"


def test_hg19_location_dict_loaded_and_differs_from_hg38():
    assert chromosomal_location_dic_hg19[GENE_ACCESSION] == ("15", 74708980, 74726001)
    assert chromosomal_location_dic[GENE_ACCESSION] == ("15", 74409289, 74433704)


def test_gene_query_without_hrc_uses_hg38_coords(monkeypatch):
    monkeypatch.setattr(helper_resolver, "map_gene", lambda gene: GENE_ACCESSION)
    assert helper_resolver.gene_query("ANYGENE") == {
        "bool": {
            "filter": [
                {"term": {"chr": "15"}},
                {"range": {"pos": {"gte": 74409289, "lte": 74433704}}},
            ]
        }
    }


def test_gene_query_with_hrc_uses_hg19_coords_and_fields(monkeypatch):
    monkeypatch.setattr(helper_resolver, "map_gene", lambda gene: GENE_ACCESSION)
    assert helper_resolver.gene_query("ANYGENE", search_hrc=True) == {
        "bool": {
            "filter": [
                {"term": {"chr_hg19.keyword": "15"}},
                {"range": {"pos_hg19": {"gte": 74708980, "lte": 74726001}}},
                {"term": {"Mapped_in_HRC.keyword": "Y"}},
            ]
        }
    }
