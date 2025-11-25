from typing import Any, AsyncGenerator
from src.config.es import es
from src.config.settings import settings
from src.graphql.models.annotation_model import FilterArgs
from src.graphql.resolvers.helper_resolver import (
    IDs_query,
    chromosome_query,
    rsIDs_query,
    gene_query,
)
from src.data_access_object.keyword_search import keyword_query_for_fields_with_filters


async def _stream_search_with_pit(
    es_fields: list[str],
    query: dict,
    max_results: int,
    batch_size: int = 10000,
) -> AsyncGenerator[Any, None]:
    """
    Generic streaming search using Point in Time API.

    Params: es_fields: List of fields to be returned in elasticsearch query
            query: Elasticsearch query object
            max_results: Maximum number of results to stream
            batch_size: Number of results per batch

    Yields: Individual SNP records
    """
    pit_id: str | None = None
    try:
        # Create PIT
        pit_response = await es.open_point_in_time(
            index=settings.ES_INDEX, keep_alive="5m"
        )
        pit_id = pit_response["id"]

        search_after = None
        total_fetched = 0

        while total_fetched < max_results:
            remaining = max_results - total_fetched
            size = min(batch_size, remaining)

            search_body = {
                "size": size,
                "query": query,
                "pit": {"id": pit_id, "keep_alive": "1m"},
                "sort": ["_shard_doc"],
                "_source": es_fields,
            }
            if search_after:
                search_body["search_after"] = search_after

            # Execute search
            resp = await es.search(body=search_body)
            hits = resp["hits"]["hits"]
            if not hits:
                break

            # Update PIT id (ES can return a refreshed id)
            pit_id = resp.get("pit_id", pit_id)

            for snp in hits:
                yield snp
                total_fetched += 1
                if total_fetched >= max_results:
                    break
            search_after = hits[-1]["sort"]
    finally:
        if pit_id:
            try:
                await es.close_point_in_time(body={"id": pit_id})
            except Exception:
                pass


async def stream_by_chromosome(
    es_fields: list[str],
    chr: str,
    start: int,
    end: int,
    max_results: int,
    filter_args: FilterArgs | None = None,
    batch_size: int = 10000,
) -> AsyncGenerator[Any, None]:
    """
    Stream annotations by chromosome with start and end range of pos.

    Params: es_fields: List of fields to be returned in elasticsearch query
            chr: Chromosome number
            start: Start position
            end: End position
            max_results: Maximum number of results to stream
            filter_args: FilterArgs object for field exists filter
            batch_size: Number of results per batch

    Yields: Individual SNP records
    """
    query = chromosome_query(chr, start, end, filter_args)
    async for snp in _stream_search_with_pit(es_fields, query, max_results, batch_size):
        yield snp


async def stream_by_rsIDs(
    es_fields: list[str],
    rsIDs: list[str],
    max_results: int,
    filter_args: FilterArgs | None = None,
    batch_size: int = 10000,
) -> AsyncGenerator[Any, None]:
    """
    Stream annotations by list of rsIDs.

    Params: es_fields: List of fields to be returned in elasticsearch query
            rsIDs: List of rsIDs of snps
            max_results: Maximum number of results to stream
            filter_args: FilterArgs object for field exists filter
            batch_size: Number of results per batch

    Yields: Individual SNP records
    """
    query = rsIDs_query(rsIDs, filter_args)
    async for snp in _stream_search_with_pit(es_fields, query, max_results, batch_size):
        yield snp


async def stream_by_IDs(
    es_fields: list[str],
    ids: list[str],
    max_results: int,
    filter_args: FilterArgs | None = None,
    batch_size: int = 10000,
) -> AsyncGenerator[Any, None]:
    """
    Stream annotations by IDs.

    Params: es_fields: List of fields to be returned in elasticsearch query
            ids: List of IDs of snps
            max_results: Maximum number of results to stream
            filter_args: FilterArgs object for field exists filter
            batch_size: Number of results per batch

    Yields: Individual SNP records
    """
    query = IDs_query(ids, filter_args)
    async for snp in _stream_search_with_pit(es_fields, query, max_results, batch_size):
        yield snp


async def stream_by_keyword(
    es_fields: list[str],
    keyword: str,
    max_results: int,
    keyword_fields: list[str] | None = None,
    filter_fields: list[str] | None = None,
    batch_size: int = 10000,
) -> AsyncGenerator[Any, None]:
    """
    Stream annotations by keyword.

    Params: es_fields: List of fields to be returned in elasticsearch query
            keyword: Keyword to be searched
            max_results: Maximum number of results to stream
            keyword_fields: Fields to search keyword in
            filter_fields: Fields that must exist
            batch_size: Number of results per batch

    Yields: Individual SNP records
    """
    query = keyword_query_for_fields_with_filters(
        keyword,
        keyword_fields,  # type: ignore
        filter_fields,  # type: ignore
    )
    async for snp in _stream_search_with_pit(es_fields, query, max_results, batch_size):
        yield snp


async def stream_by_gene_product(
    es_fields: list[str],
    gene: str,
    max_results: int,
    filter_args: FilterArgs | None = None,
    batch_size: int = 10000,
) -> AsyncGenerator[Any, None]:
    """
    Stream annotations by gene product.

    Params: es_fields: List of fields to be returned in elasticsearch query
            gene: Gene product
            max_results: Maximum number of results to stream
            filter_args: FilterArgs object for field exists filter
            batch_size: Number of results per batch

    Yields: Individual SNP records
    """
    query = gene_query(gene, filter_args)

    if query is None:
        return

    async for snp in _stream_search_with_pit(es_fields, query, max_results, batch_size):
        yield snp
