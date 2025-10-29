from src.config.es import es
from src.config.settings import settings
from src.graphql.models.annotation_model import FilterArgs, PageArgs
from src.graphql.resolvers.helper_resolver import (
    IDs_query,
    chromosome_query,
    rsIDs_query,
    gene_query,
)
from src.data_access_object.keyword_search import keyword_query_for_fields_with_filters
from src.graphql.resolvers.api_snp_helper_resolver import (
    output_error_msg,
    convert_hits_to_output,
)


async def _execute_search(
    es_fields: list[str],
    query: dict,
    page_args: PageArgs,
    error_message: str,
):
    """
    Generic search execution function to eliminate code duplication.

    Params: es_fields: List of fields to be returned in elasticsearch query
            query: Elasticsearch query object
            page_args: PageArgs object for pagination
            error_message: Custom error message for this operation

    Returns: OutputSnpInfo with list of Snps
    """
    try:
        resp = await es.search(
            index=settings.ES_INDEX,
            source=es_fields,  # type: ignore
            from_=page_args.from_,
            size=page_args.size,
            query=query,
        )
        return convert_hits_to_output(es_fields, resp["hits"]["hits"])
    except Exception:
        return output_error_msg(error_message)


async def search_by_chromosome(
    es_fields: list[str],
    chr: str,
    start: int,
    end: int,
    page_args: PageArgs,
    filter_args: FilterArgs | None = None,
):
    """
    Query for getting annotation by chromosome with start and end range of pos

    Params: es_fields: List of fields to be returned in elasticsearch query
            chr: Chromosome number
            start: Start position
            end: End position
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter

    Returns: OutputSnpInfo with list of Snps
    """
    page_args = page_args or PageArgs()
    query = chromosome_query(chr, start, end, filter_args)
    return await _execute_search(
        es_fields,
        query,
        page_args,
        "Unable to retrieve information for search by chromosome",
    )


async def search_by_rsIDs(
    es_fields: list[str],
    rsIDs: list[str],
    page_args: PageArgs,
    filter_args: FilterArgs | None = None,
):
    """
    Query for getting annotation by list of rsIDs

    Params: es_fields: List of fields to be returned in elasticsearch query
            rsIDs: List of rsIDs of snps
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter

    Returns: OutputSnpInfo with list of Snps
    """
    page_args = page_args or PageArgs()
    query = rsIDs_query(rsIDs, filter_args)
    return await _execute_search(
        es_fields,
        query,
        page_args,
        "Unable to retrieve information for search by RSIDS",
    )


async def search_by_IDs(
    es_fields: list[str],
    ids: list[str],
    page_args: PageArgs,
    filter_args: FilterArgs | None = None,
):
    """
    Query for getting annotation by IDs

    Params: es_fields: List of fields to be returned in elasticsearch query
            ids: List of IDs of snps
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter

    Returns: OutputSnpInfo with list of Snps
    """
    page_args = page_args or PageArgs()
    query = IDs_query(ids, filter_args)
    return await _execute_search(
        es_fields,
        query,
        page_args,
        "Unable to retrieve information for search by IDS",
    )


async def search_by_keyword(
    es_fields: list[str],
    keyword: str,
    page_args: PageArgs,
    keyword_fields: list[str] | None = None,
    filter_fields: list[str] | None = None,
):
    """
    Query for getting annotation by keyword

    Params: es_fields: List of fields to be returned in elasticsearch query
            keyword: Keyword to be searched
            page_args: PageArgs object for pagination
            keyword_fields: Fields to search keyword in
            filter_fields: Fields that must exist

    Returns: OutputSnpInfo with list of Snps
    """
    page_args = page_args or PageArgs()
    query = keyword_query_for_fields_with_filters(
        keyword,
        keyword_fields,  # type: ignore
        filter_fields,  # type: ignore
    )
    return await _execute_search(
        es_fields,
        query,
        page_args,
        "Unable to retrieve information for search by keyword",
    )


async def search_by_gene_product(
    es_fields: list[str],
    gene: str,
    page_args: PageArgs,
    filter_args: FilterArgs | None = None,
):
    """
    Query for getting annotation by gene product

    Params: es_fields: List of fields to be returned in elasticsearch query
            gene: Gene product
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter

    Returns: OutputSnpInfo with list of Snps
    """
    page_args = page_args or PageArgs()
    query = gene_query(gene, filter_args)

    if query is None:
        return output_error_msg(
            "Unable to construct query for search by gene product operation"
        )

    return await _execute_search(
        es_fields,
        query,
        page_args,
        "Unable to retrieve information for search by gene product",
    )
