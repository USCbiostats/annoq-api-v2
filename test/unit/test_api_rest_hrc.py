"""Unit tests: the REST api resolvers thread search_hrc into the query builders.

The builders themselves are covered in test_query_builders_hrc.py; here we only
prove the flag is passed through. Builders/ES are monkeypatched so no ES is needed.
"""

import asyncio

import src.graphql.resolvers.api_snp_resolver as api_snp
import src.graphql.resolvers.api_count_resolver as api_count
from src.graphql.models.annotation_model import PageArgs


class _FakeES:
    async def count(self, **kwargs):
        return {"count": 0}


def _spy(store):
    def builder(*args, filter_args=None, search_hrc=None, **kwargs):
        # The resolvers call the builders with search_hrc as the final positional arg.
        if search_hrc is None and args:
            search_hrc = args[-1]
        store["search_hrc"] = search_hrc
        return {"match_none": {}}

    return builder


# --- api_snp_resolver ------------------------------------------------------
def test_api_search_by_chromosome_threads_search_hrc(monkeypatch):
    store = {}
    monkeypatch.setattr(api_snp, "chromosome_query", _spy(store))
    monkeypatch.setattr(api_snp, "_execute_search", _passthrough_execute)
    asyncio.run(api_snp.search_by_chromosome(["chr"], "18", 1, 100, PageArgs(), None, search_hrc=True))
    assert store["search_hrc"] is True


def test_api_search_by_rsIDs_threads_search_hrc(monkeypatch):
    store = {}
    monkeypatch.setattr(api_snp, "rsIDs_query", _spy(store))
    monkeypatch.setattr(api_snp, "_execute_search", _passthrough_execute)
    asyncio.run(api_snp.search_by_rsIDs(["chr"], ["rs1"], PageArgs(), None, search_hrc=True))
    assert store["search_hrc"] is True


def test_api_search_by_gene_product_threads_search_hrc(monkeypatch):
    store = {}
    monkeypatch.setattr(api_snp, "gene_query", _spy(store))
    monkeypatch.setattr(api_snp, "_execute_search", _passthrough_execute)
    asyncio.run(api_snp.search_by_gene_product(["chr"], "ANYGENE", PageArgs(), None, search_hrc=True))
    assert store["search_hrc"] is True


async def _passthrough_execute(es_fields, query, page_args, error_message):
    return query


# --- api_count_resolver ----------------------------------------------------
def test_api_count_by_chromosome_threads_search_hrc(monkeypatch):
    store = {}
    monkeypatch.setattr(api_count, "chromosome_query", _spy(store))
    monkeypatch.setattr(api_count, "es", _FakeES())
    asyncio.run(api_count.count_by_chromosome("18", 1, 100, None, search_hrc=True))
    assert store["search_hrc"] is True


def test_api_count_by_rsIDs_threads_search_hrc(monkeypatch):
    store = {}
    monkeypatch.setattr(api_count, "rsIDs_query", _spy(store))
    monkeypatch.setattr(api_count, "es", _FakeES())
    asyncio.run(api_count.count_by_rsIDs(["rs1"], None, search_hrc=True))
    assert store["search_hrc"] is True


def test_api_count_by_gene_product_threads_search_hrc(monkeypatch):
    store = {}
    monkeypatch.setattr(api_count, "gene_query", _spy(store))
    monkeypatch.setattr(api_count, "es", _FakeES())
    asyncio.run(api_count.count_by_gene_product("ANYGENE", None, search_hrc=True))
    assert store["search_hrc"] is True
