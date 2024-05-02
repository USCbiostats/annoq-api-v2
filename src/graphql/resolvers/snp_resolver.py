from src.config.es import es
from src.config.settings import settings
from src.graphql.resolvers.download_resolver import download_annotations
from src.graphql.models.annotation_model import FilterArgs, Histogram, PageArgs, QueryType
from src.graphql.resolvers.helper_resolver import IDs_query, annotation_query, chromosome_query, convert_aggs, convert_hits, convert_scroll_hits, gene_query, get_aggregation_query, rsID_query, rsIDs_query


async def get_annotations(es_fields: list[str], query_type: str, histogram=Histogram):
    """ 
    Query for getting all annotations, no filter, size 20

    Params: es_fields: List of fields to be returned in elasticsearch query
            query_type: Type of query to be executed
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          query = annotation_query(),
          aggs = await get_aggregation_query(es_fields, histogram) if query_type == QueryType.AGGS else None,
          size = 20,
          scroll = '2m' if query_type == QueryType.DOWNLOAD else None
    )

    if query_type == QueryType.DOWNLOAD:
      url = await download_annotations(es_fields, resp)
      return url
    
    elif query_type == QueryType.SNPS:
      results = convert_hits(resp['hits']['hits'])  
      return results
    
    elif query_type == QueryType.AGGS:
      results = convert_aggs(resp['aggregations'])  
      return results
    

async def scroll_annotations_(es_fields: list[str], scroll_id: str=None):
    """ 
    Query for getting all annotations, no filter, with scrolling

    Params: es_fields: List of fields to be returned in elasticsearch query
            scroll_id: Scroll id for scrolling

    Returns: ScrollSnp object
    """
    if scroll_id != None:
      resp = await es.scroll(
              scroll = '2m',
              scroll_id = scroll_id
        )
    else:
      resp = await es.search(
              index = settings.ES_INDEX,
              source = es_fields,
              query = annotation_query(),
              scroll = '2m'
        )
    results = convert_scroll_hits(resp['hits']['hits'], resp['_scroll_id'])
    return results


async def search_by_chromosome(es_fields: list[str], chr: str, start: int, end: int, query_type: str, page_args=PageArgs, filter_args=FilterArgs,
                               histogram=Histogram):
    """ 
    Query for getting annotation by chromosome with start and end range of pos

    Params: es_fields: List of fields to be returned in elasticsearch query
            chr: Chromosome number
            start: Start position
            end: End position
            query_type: Type of query to be executed
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
      page_args = PageArgs

    if histogram is None:
      histogram = Histogram

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_ if query_type != QueryType.DOWNLOAD else None,
          size = page_args.size,
          query = chromosome_query(chr, start, end, filter_args),
          aggs = await get_aggregation_query(es_fields, histogram) if query_type == QueryType.AGGS else None,
          scroll = '2m' if query_type == QueryType.DOWNLOAD else None
    )

    if query_type == QueryType.DOWNLOAD:
      url = await download_annotations(es_fields, resp)
      return url

    elif query_type == QueryType.SNPS:
      results = convert_hits(resp['hits']['hits'])  
      return results
    
    elif query_type == QueryType.AGGS:
      results = convert_aggs(resp['aggregations']) 
      return results
    

async def scroll_by_chromosome(es_fields: list[str], chr: str, start: int, end: int, scroll_id: str=None):
    """ 
    Query for getting annotation by chromosome with start and end range of pos with scrolling

    Params: es_fields: List of fields to be returned in elasticsearch query
            chr: Chromosome number
            start: Start position
            end: End position
            scroll_id: Scroll id for scrolling

    Returns: ScrollSnp object
    """
    if scroll_id != None:
      resp = await es.scroll(
              scroll = '2m',
              scroll_id = scroll_id
        )
    else:
      resp = await es.search(
              index = settings.ES_INDEX,
              source = es_fields,
              query = chromosome_query(chr, start, end),
              scroll = '2m'
        )
    results = convert_scroll_hits(resp['hits']['hits'], resp['_scroll_id'])
    return results


async def search_by_rsID(es_fields: list[str], rsID:str, query_type: str, page_args=PageArgs, filter_args=FilterArgs, histogram=Histogram):
    """ 
    Query for getting annotation by rsID

    Params: es_fields: List of fields to be returned in elasticsearch query
            rsID: rsID of snp
            query_type: Type of query to be executed
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
      page_args = PageArgs

    if histogram is None:
      histogram = Histogram

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_ if query_type != QueryType.DOWNLOAD else None,
          size = page_args.size,
          query = rsID_query(rsID, filter_args),
          aggs = await get_aggregation_query(es_fields, histogram) if query_type == QueryType.AGGS else None,
          scroll = '2m' if query_type == QueryType.DOWNLOAD else None
    )

    if query_type == QueryType.DOWNLOAD:
      url = await download_annotations(es_fields, resp)
      return url

    elif query_type == QueryType.SNPS:
      results = convert_hits(resp['hits']['hits'])  
      return results
    
    elif query_type == QueryType.AGGS:
      results = convert_aggs(resp['aggregations'])  
      return results
    

async def scroll_by_rsID(es_fields: list[str], rsID:str, scroll_id: str=None):
    """ 
    Query for getting annotation by rsID with scrolling

    Params: es_fields: List of fields to be returned in elasticsearch query
            rsID: rsID of snp
            scroll_id: Scroll id for scrolling

    Returns: ScrollSnp object
    """
    if scroll_id != None:
      resp = await es.scroll(
              scroll = '2m',
              scroll_id = scroll_id
        )
    else:
      resp = await es.search(
              index = settings.ES_INDEX,
              source = es_fields,
              query = rsID_query(rsID),
              scroll = '2m'
        )
    results = convert_scroll_hits(resp['hits']['hits'], resp['_scroll_id'])
    return results
    

async def search_by_rsIDs(es_fields: list[str], rsIDs: list[str], query_type: str, page_args=PageArgs, filter_args=FilterArgs, histogram=Histogram):
    """ 
    Query for getting annotation by list of rsIDs

    Params: es_fields: List of fields to be returned in elasticsearch query
            rsIDs: List of rsIDs of snps
            query_type: Type of query to be executed
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
      page_args = PageArgs

    if histogram is None:
      histogram = Histogram

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_ if query_type != QueryType.DOWNLOAD else None,
          size = page_args.size,
          query = rsIDs_query(rsIDs, filter_args),
          aggs = await get_aggregation_query(es_fields, histogram) if query_type == QueryType.AGGS else None,
          scroll = '2m' if query_type == QueryType.DOWNLOAD else None
    )
    
    if query_type == QueryType.DOWNLOAD:
      url = await download_annotations(es_fields, resp)
      return url

    elif query_type == QueryType.SNPS:
      results = convert_hits(resp['hits']['hits'])  
      return results
    
    elif query_type == QueryType.AGGS:
      results = convert_aggs(resp['aggregations'])  
      return results


async def scroll_by_rsIDs(es_fields: list[str], rsIDs: list[str], scroll_id: str=None):
    """ 
    Query for getting annotation by rsIDs with scrolling

    Params: es_fields: List of fields to be returned in elasticsearch query
            rsIDs: List of rsIDs of snps
            scroll_id: Scroll id for scrolling

    Returns: ScrollSnp object
    """
    if scroll_id != None:
      resp = await es.scroll(
              scroll = '2m',
              scroll_id = scroll_id
        )
    else:
      resp = await es.search(
              index = settings.ES_INDEX,
              source = es_fields,
              query = rsIDs_query(rsIDs),
              scroll = '2m'
        )
    results = convert_scroll_hits(resp['hits']['hits'], resp['_scroll_id'])
    return results


# query for VCF file
async def search_by_IDs(es_fields: list[str], ids: list[str], query_type: str, page_args=PageArgs, filter_args=FilterArgs, histogram=Histogram):
    """ 
    Query for getting annotation by IDs

    Params: es_fields: List of fields to be returned in elasticsearch query
            ids: List of IDs of snps
            query_type: Type of query to be executed
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
      page_args = PageArgs

    if histogram is None:
      histogram = Histogram

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_ if query_type != QueryType.DOWNLOAD else None,
          size = page_args.size,
          query = IDs_query(ids, filter_args),
          aggs = await get_aggregation_query(es_fields, histogram) if query_type == QueryType.AGGS else None,
          scroll = '2m' if query_type == QueryType.DOWNLOAD else None
    )
    
    if query_type == QueryType.DOWNLOAD:
      url = await download_annotations(es_fields, resp)
      return url

    elif query_type == QueryType.SNPS:
      results = convert_hits(resp['hits']['hits'])  
      return results
    
    elif query_type == QueryType.AGGS:
        results = convert_aggs(resp['aggregations'])  
        return results
    

async def scroll_by_IDs(es_fields: list[str], ids: list[str], scroll_id: str=None):
    """ 
    Query for getting annotation by IDs with scrolling

    Params: es_fields: List of fields to be returned in elasticsearch query
            ids: List of IDs of snps
            scroll_id: Scroll id for scrolling

    Returns: ScrollSnp object
    """
    if scroll_id != None:
      resp = await es.scroll(
              scroll = '2m',
              scroll_id = scroll_id
        )
    else:
      resp = await es.search(
              index = settings.ES_INDEX,
              source = es_fields,
              query = IDs_query(ids),
              scroll = '2m'
        )
    results = convert_scroll_hits(resp['hits']['hits'], resp['_scroll_id'])
    return results


# query for gene product
async def search_by_gene(es_fields: list[str], gene:str, query_type: str, page_args=PageArgs, filter_args=FilterArgs, histogram=Histogram):
    """ 
    Query for getting annotation by gene product

    Params: es_fields: List of fields to be returned in elasticsearch query
            gene: Gene product
            query_type: Type of query to be executed
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter
            histogram: Histogram object for aggregation query

    Returns: List of Snps
    """
    if page_args is None:
      page_args = PageArgs

    if histogram is None:
      histogram = Histogram

    query = gene_query(gene, filter_args)

    if query is not None:
      resp = await es.search(
              index = settings.ES_INDEX,
              source = es_fields,
              from_= page_args.from_ if query_type != QueryType.DOWNLOAD else None,
              size = page_args.size,
              query = query,
              aggs = await get_aggregation_query(es_fields, histogram) if query_type == QueryType.AGGS else None,
              scroll = '2m' if query_type == QueryType.DOWNLOAD else None
      )
      
      if query_type == QueryType.DOWNLOAD:
        url = await download_annotations(es_fields, resp)
        return url

      elif query_type == QueryType.SNPS:
        results = convert_hits(resp['hits']['hits'])  
        return results
  
      elif query_type == QueryType.AGGS:
        results = convert_aggs(resp['aggregations'])  
        return results
      
async def scroll_by_gene(es_fields: list[str], gene:str, scroll_id: str=None):
    """ 
    Query for getting annotation by gene product with scrolling

    Params: es_fields: List of fields to be returned in elasticsearch query
            gene: Gene product
            scroll_id: Scroll id for scrolling

    Returns: ScrollSnp object
    """
    if scroll_id != None:
      resp = await es.scroll(
              scroll = '2m',
              scroll_id = scroll_id
        )
    else:
      query = gene_query(gene)
      if query is not None:
        resp = await es.search(
                index = settings.ES_INDEX,
                source = es_fields,
                query = query,
                scroll = '2m'
          )
    results = convert_scroll_hits(resp['hits']['hits'], resp['_scroll_id'])
    return results