from src.config.es import es
from src.config.settings import settings
from src.graphql.models.annotation_model import FilterArgs, PageArgs
from src.graphql.resolvers.helper_resolver import IDs_query, chromosome_query, rsIDs_query, keyword_query, gene_query
from src.graphql.resolvers.api_snp_helper_resolver import output_error_msg, convert_scroll_hits


async def search_by_chromosome(es_fields: list[str], chr: str, start: int, end: int, page_args=PageArgs, filter_args=FilterArgs):
    """ 
    Query for getting annotation by chromosome with start and end range of pos

    Params: es_fields: List of fields to be returned in elasticsearch query
            chr: Chromosome number
            start: Start position
            end: End position
            query_type: Type of query to be executed
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter


    Returns: List of Snps
    """
    if page_args is None:
      page_args = PageArgs

    try:
        resp = await es.search(
            index = settings.ES_INDEX,
            source = es_fields,
            from_= page_args.from_,
            size = page_args.size,
            query = chromosome_query(chr, start, end, filter_args)
        )

        return await query_return(es_fields, resp)
    # except ConnectionError as e:
    #     return OutputSnpInfo(operationInfo= BaseOutput(success = False, message = e.message), details = None)
    except Exception:
        return output_error_msg("Unable to retrieve information for search by chromosome")
        


async def search_by_rsIDs(es_fields: list[str], rsIDs: list[str], page_args=PageArgs, filter_args=FilterArgs):
    """ 
    Query for getting annotation by list of rsIDs

    Params: es_fields: List of fields to be returned in elasticsearch query
            rsIDs: List of rsIDs of snps
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter

    Returns: List of Snps
    """
    if page_args is None:
      page_args = PageArgs

    try:
      resp = await es.search(
            index = settings.ES_INDEX,
            source = es_fields,
            from_= page_args.from_, 
            size = page_args.size,
            query = rsIDs_query(rsIDs, filter_args),
      )
      return await query_return(es_fields, resp)
    except Exception:
        return output_error_msg("Unable to retrieve information for search by RSIDS")

  
  

async def search_by_IDs(es_fields: list[str], ids: list[str],  page_args=PageArgs, filter_args=FilterArgs):
    """ 
    Query for getting annotation by IDs

    Params: es_fields: List of fields to be returned in elasticsearch query
            ids: List of IDs of snps
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter


    Returns: List of Snps
    """
    if page_args is None:
      page_args = PageArgs

    try:
      resp = await es.search(
            index = settings.ES_INDEX,
            source = es_fields,
            from_= page_args.from_,
            size = page_args.size,
            query = IDs_query(ids, filter_args),
      )
      
      return await query_return(es_fields, resp)
    except Exception:
        return output_error_msg("Unable to retrieve information for search by IDS")
  
  
async def search_by_keyword(es_fields: list[str], keyword: str, page_args=PageArgs):
    """ 
    Query for getting annotation by keyword

    Params: es_fields: List of fields to be returned in elasticsearch query
            keyword: Keyword to be searched
            page_args: PageArgs object for pagination

    Returns: List of Snps
    """
    if page_args is None:
      page_args = PageArgs
    try:
      
      resp = await es.search(
            index = settings.ES_INDEX,
            source = es_fields,
            from_= page_args.from_ ,
            size = page_args.size,
            query = keyword_query(keyword)
      )
    
      return await query_return(es_fields, resp)
    except Exception:
        return output_error_msg("Unable to retrieve information for search by keyword")
  
  
async def search_by_gene(es_fields: list[str], gene:str, page_args=PageArgs, filter_args=FilterArgs):
    """ 
    Query for getting annotation by gene product

    Params: es_fields: List of fields to be returned in elasticsearch query
            gene: Gene product
            page_args: PageArgs object for pagination
            filter_args: FilterArgs object for field exists filter

    Returns: List of Snps
    """
    if page_args is None:
      page_args = PageArgs


    query = gene_query(gene, filter_args)
    try:
      
      if query is not None:
        resp = await es.search(
                index = settings.ES_INDEX,
                source = es_fields,
                from_= page_args.from_,
                size = page_args.size,
                query = query
        )
      else:
        return output_error_msg("Unable to construct query for search by gene operation")
        
      return await query_return(es_fields, resp)
    except Exception:
        return output_error_msg("Unable to retrieve information for search by gene")


async def query_return(es_fields, resp):
    """
    Common return function for all queries

    Params: es_fields: List of fields to be returned in elasticsearch query
            resp: Response from elasticsearch query
    """
    results = convert_scroll_hits(resp['hits']['hits'])  
    return results


