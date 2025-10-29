from src.config.es import es
from src.config.settings import settings
from src.graphql.resolvers.download_resolver import download_annotations_from_stream
from src.graphql.models.annotation_model import (
    FilterArgs,
    Histogram,
    PageArgs,
    QueryType,
)
from src.graphql.resolvers.helper_resolver import (
    IDs_query,
    annotation_query,
    chromosome_query,
    keyword_query,
    convert_aggs,
    convert_scroll_hits,
    gene_query,
    get_aggregation_query,
    get_default_aggregation_fields,
    rsID_query,
    rsIDs_query,
)
from src.data_access_object.keyword_search import keyword_query_for_fields_with_filters
from src.graphql.resolvers import large_result_streaming_resolver


async def query_return(query_type, es_fields, resp):
    """
    Common return function for all queries

    Params: query_type: Type of query to be executed
            es_fields: List of fields to be returned in elasticsearch query
            resp: Response from elasticsearch query
    """
    if query_type == QueryType.SCROLL:
        results = convert_scroll_hits(resp["hits"]["hits"], resp["_scroll_id"])
        return results

    elif query_type == QueryType.SNPS:
        results = convert_scroll_hits(resp["hits"]["hits"], None)
        return results

    elif query_type == QueryType.AGGS:
        results = convert_aggs(resp["aggregations"])
        return results


async def get_annotations(
    es_fields: list[str],
    query_type: str,
    aggregation_fields: list[tuple[str, list[str]]] | None = None,
    histogram=Histogram(),
):
    """
    Query for getting all annotations, no filter, size 20

    Params: es_fields: List of fields to be returned in elasticsearch query
            query_type: Type of query to be executed
            aggregation_fields: List of fields for aggregation, along with their subfields
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    resp = await es.search(
        index=settings.ES_INDEX,
        source=es_fields,  # type: ignore
        query=annotation_query(),
        aggs=await get_aggregation_query(
            aggregation_fields or get_default_aggregation_fields(es_fields), histogram
        )
        if query_type == QueryType.AGGS
        else None,
        size=20,
        scroll="2m" if query_type == QueryType.DOWNLOAD else None,
    )

    return await query_return(query_type, es_fields, resp)


async def scroll_annotations_(scroll_id: str):
    """
    Query for getting all annotations, no filter, with scrolling

    Params: scroll_id: Scroll id for scrolling

    Returns: ScrollSnp object
    """
    resp = await es.scroll(scroll="2m", scroll_id=scroll_id)
    results = convert_scroll_hits(resp["hits"]["hits"], resp["_scroll_id"])
    return results


async def search_by_chromosome(
    es_fields: list[str],
    chr: str,
    start: int,
    end: int,
    query_type: str,
    aggregation_fields: list[tuple[str, list[str]]] | None = None,
    page_args=PageArgs(),
    filter_args=FilterArgs(),
    histogram=Histogram(),
):
    """
    Query for getting annotation by chromosome with start and end range of pos

    Params: es_fields: List of fields to be returned in elasticsearch query
            chr: Chromosome number
            start: Start position
            end: End position
            query_type: Type of query to be executed
            aggregation_fields: List of fields for aggregation, along with their subfields
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
        page_args = PageArgs()

    if histogram is None:
        histogram = Histogram()

    if query_type == QueryType.DOWNLOAD:
        stream = large_result_streaming_resolver.stream_by_chromosome(
            es_fields, chr, start, end, settings.SIZE_DOWNLOAD_SIZE, filter_args
        )
        return await download_annotations_from_stream(es_fields, stream)

    resp = await es.search(
        index=settings.ES_INDEX,
        source=es_fields,  # type: ignore
        from_=page_args.from_ if query_type != QueryType.SCROLL else None,
        size=page_args.size,
        query=chromosome_query(chr, start, end, filter_args),
        aggs=await get_aggregation_query(
            aggregation_fields or get_default_aggregation_fields(es_fields), histogram
        )
        if query_type == QueryType.AGGS
        else None,
        scroll="2m" if query_type == QueryType.SCROLL else None,
    )

    return await query_return(query_type, es_fields, resp)


async def search_by_rsID(
    es_fields: list[str],
    rsID: str,
    query_type: str,
    aggregation_fields: list[tuple[str, list[str]]] | None = None,
    page_args=PageArgs(),
    filter_args=FilterArgs(),
    histogram=Histogram(),
):
    """
    Query for getting annotation by rsID

    Params: es_fields: List of fields to be returned in elasticsearch query
            rsID: rsID of snp
            query_type: Type of query to be executed
            aggregation_fields: List of fields for aggregation, along with their subfields
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
        page_args = PageArgs()

    if histogram is None:
        histogram = Histogram()

    if query_type == QueryType.DOWNLOAD:
        stream = large_result_streaming_resolver.stream_by_rsIDs(
            es_fields, [rsID], settings.SIZE_DOWNLOAD_SIZE, filter_args
        )
        return await download_annotations_from_stream(es_fields, stream)

    resp = await es.search(
        index=settings.ES_INDEX,
        source=es_fields,  # type: ignore
        from_=page_args.from_ if query_type != QueryType.SCROLL else None,
        size=page_args.size,
        query=rsID_query(rsID, filter_args),
        aggs=await get_aggregation_query(
            aggregation_fields or get_default_aggregation_fields(es_fields), histogram
        )
        if query_type == QueryType.AGGS
        else None,
        scroll="2m" if query_type == QueryType.SCROLL else None,
    )

    return await query_return(query_type, es_fields, resp)


async def search_by_rsIDs(
    es_fields: list[str],
    rsIDs: list[str],
    query_type: str,
    aggregation_fields: list[tuple[str, list[str]]] | None = None,
    page_args=PageArgs(),
    filter_args=FilterArgs(),
    histogram=Histogram(),
):
    """
    Query for getting annotation by list of rsIDs

    Params: es_fields: List of fields to be returned in elasticsearch query
            rsIDs: List of rsIDs of snps
            query_type: Type of query to be executed
            aggregation_fields: List of fields for aggregation, along with their subfields
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
        page_args = PageArgs()

    if histogram is None:
        histogram = Histogram()

    if query_type == QueryType.DOWNLOAD:
        stream = large_result_streaming_resolver.stream_by_rsIDs(
            es_fields, rsIDs, settings.SIZE_DOWNLOAD_SIZE, filter_args
        )
        return await download_annotations_from_stream(es_fields, stream)

    resp = await es.search(
        index=settings.ES_INDEX,
        source=es_fields,  # type: ignore
        from_=page_args.from_ if query_type != QueryType.SCROLL else None,
        size=page_args.size,
        query=rsIDs_query(rsIDs, filter_args),
        aggs=await get_aggregation_query(
            aggregation_fields or get_default_aggregation_fields(es_fields), histogram
        )
        if query_type == QueryType.AGGS
        else None,
        scroll="2m" if query_type == QueryType.SCROLL else None,
    )

    return await query_return(query_type, es_fields, resp)


# query for VCF file
async def search_by_IDs(
    es_fields: list[str],
    ids: list[str],
    query_type: str,
    aggregation_fields: list[tuple[str, list[str]]] | None = None,
    page_args=PageArgs(),
    filter_args=FilterArgs(),
    histogram=Histogram(),
):
    """
    Query for getting annotation by IDs

    Params: es_fields: List of fields to be returned in elasticsearch query
            ids: List of IDs of snps
            query_type: Type of query to be executed
            aggregation_fields: List of fields for aggregation, along with their subfields
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
        page_args = PageArgs()

    if histogram is None:
        histogram = Histogram()

    if query_type == QueryType.DOWNLOAD:
        stream = large_result_streaming_resolver.stream_by_IDs(
            es_fields, ids, settings.SIZE_DOWNLOAD_SIZE, filter_args
        )
        return await download_annotations_from_stream(es_fields, stream)

    resp = await es.search(
        index=settings.ES_INDEX,
        source=es_fields,  # type: ignore
        from_=page_args.from_ if query_type != QueryType.SCROLL else None,
        size=page_args.size,
        query=IDs_query(ids, filter_args),
        aggs=await get_aggregation_query(
            aggregation_fields or get_default_aggregation_fields(es_fields), histogram
        )
        if query_type == QueryType.AGGS
        else None,
        scroll="2m" if query_type == QueryType.SCROLL else None,
    )

    return await query_return(query_type, es_fields, resp)


async def search_by_gene(
    es_fields: list[str],
    gene: str,
    query_type: str,
    aggregation_fields: list[tuple[str, list[str]]] | None = None,
    page_args=PageArgs(),
    filter_args=FilterArgs(),
    histogram=Histogram(),
):
    """
    Query for getting annotation by gene product

    Params: es_fields: List of fields to be returned in elasticsearch query
            gene: Gene product
            query_type: Type of query to be executed
            page_args: PageArgs object for pagination
            aggregation_fields: List of fields for aggregation, along with their subfields
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
        page_args = PageArgs()

    if histogram is None:
        histogram = Histogram()

    if query_type == QueryType.DOWNLOAD:
        stream = large_result_streaming_resolver.stream_by_gene_product(
            es_fields, gene, settings.SIZE_DOWNLOAD_SIZE, filter_args
        )
        return await download_annotations_from_stream(es_fields, stream)

    query = gene_query(gene, filter_args)

    if query is not None:
        resp = await es.search(
            index=settings.ES_INDEX,
            source=es_fields,  # type: ignore
            from_=page_args.from_ if query_type != QueryType.SCROLL else None,
            size=page_args.size,
            query=query,
            aggs=await get_aggregation_query(
                aggregation_fields or get_default_aggregation_fields(es_fields),
                histogram,
            )
            if query_type == QueryType.AGGS
            else None,
            scroll="2m" if query_type == QueryType.SCROLL else None,
        )

        return await query_return(query_type, es_fields, resp)


async def search_by_keyword_on_specific_fields(
    es_fields: list[str],
    keyword: str,
    query_type: str,
    aggregation_fields: list[tuple[str, list[str]]] | None = None,
    page_args=PageArgs(),
    filter_args=FilterArgs(),
    histogram=Histogram(),
    keyword_fields=list[str],
):
    """
    Query for getting annotation by keyword using specified keyword columns

    Params: es_fields: List of fields to be returned in elasticsearch query
            keyword: keyword
            query_type: Type of query to be executed
            page_args: PageArgs object for pagination
            aggregation_fields: List of fields for aggregation, along with their subfields
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query
            keyword_fields: Keyword fields for searching

    Returns: List of Snps
    """
    if page_args is None:
        page_args = PageArgs()

    if histogram is None:
        histogram = Histogram()

    filter_fields = []
    if filter_args and filter_args.exists:
        for field in filter_args.exists:
            filter_fields.append(field)

    if query_type == QueryType.DOWNLOAD:
        stream = large_result_streaming_resolver.stream_by_keyword(
            es_fields,
            keyword,
            settings.SIZE_DOWNLOAD_SIZE,
            keyword_fields,  # type: ignore
            filter_fields,
        )
        return await download_annotations_from_stream(es_fields, stream)

    resp = await es.search(
        index=settings.ES_INDEX,
        source=es_fields,  # type: ignore
        from_=page_args.from_ if query_type != QueryType.SCROLL else None,
        size=page_args.size,
        query=keyword_query_for_fields_with_filters(
            keyword,
            keyword_fields,  # type: ignore
            filter_fields,
        ),
        aggs=await get_aggregation_query(
            aggregation_fields or get_default_aggregation_fields(es_fields), histogram
        )
        if query_type == QueryType.AGGS
        else None,
        scroll="2m" if query_type == QueryType.SCROLL else None,
    )

    return await query_return(query_type, es_fields, resp)


async def search_by_keyword(
    es_fields: list[str],
    keyword: str,
    query_type: str,
    aggregation_fields: list[tuple[str, list[str]]] | None = None,
    page_args=PageArgs(),
    histogram=Histogram(),
):
    """
    Query for getting annotation by keyword

    Params: es_fields: List of fields to be returned in elasticsearch query
            keyword: Keyword to be searched
            query_type: Type of query to be executed
            aggregation_fields: List of fields for aggregation, along with their subfields
            page_args: PageArgs object for pagination
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
        page_args = PageArgs()

    if histogram is None:
        histogram = Histogram()

    if query_type == QueryType.DOWNLOAD:
        stream = large_result_streaming_resolver.stream_by_keyword(
            es_fields, keyword, settings.SIZE_DOWNLOAD_SIZE, None, None
        )
        return await download_annotations_from_stream(es_fields, stream)

    resp = await es.search(
        index=settings.ES_INDEX,
        source=es_fields,  # type: ignore
        from_=page_args.from_ if query_type != QueryType.SCROLL else None,
        size=page_args.size,
        query=keyword_query(keyword),
        aggs=await get_aggregation_query(
            aggregation_fields or get_default_aggregation_fields(es_fields), histogram
        )
        if query_type == QueryType.AGGS
        else None,
        scroll="2m" if query_type == QueryType.SCROLL else None,
    )

    return await query_return(query_type, es_fields, resp)
