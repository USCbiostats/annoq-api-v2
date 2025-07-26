from src.config.es import es
from src.config.settings import settings
from src.graphql.models.annotation_model import FilterArgs, PageArgs
from src.graphql.resolvers.helper_resolver import IDs_query, chromosome_query, rsIDs_query, gene_query
from src.data_access_object.keyword_search import keyword_query_for_fields_with_filters
from src.graphql.resolvers.api_snp_helper_resolver import output_error_msg, convert_scroll_hits
from src.graphql.models.generated.snp import SnpModel
from src.graphql.models.return_info_model import OutputSnpInfo
from src.utils import clean_field_name
from src.data_adapter.snp_attributes import get_version_info


STANDARD_PAGE_SIZE =  5000   #Elasticsearch maximum is 10000


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
            size = STANDARD_PAGE_SIZE,
            query = chromosome_query(chr, start, end, filter_args),
            scroll = '2m'     
        )

        return await query_retrieve_all_res(es_fields, resp, page_args.size, STANDARD_PAGE_SIZE)
    # except ConnectionError as e:
    #     return OutputSnpInfo(operationInfo= BaseOutput(success = False, message = e.message), details = None)
    except Exception:
      message = "Unable to retrieve information for search by chromosome"
      return output_error_msg(message)      
        


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
            size = STANDARD_PAGE_SIZE,
            query = rsIDs_query(rsIDs, filter_args),
            scroll = '2m'
      )
      return await query_retrieve_all_res(es_fields, resp, page_args.size, STANDARD_PAGE_SIZE)
    except Exception:
      message = "Unable to retrieve information for search by RSIDS"
      return output_error_msg(message)       

  
  

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
      message = "Unable to retrieve information for search by IDS"
      return output_error_msg(message)       
  
  
async def search_by_keyword(es_fields: list[str], keyword: str, page_args=PageArgs, keyword_fields: list[str] = None, filter_fields: list[str] = None):
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
            size = STANDARD_PAGE_SIZE,
            query = keyword_query_for_fields_with_filters(keyword, keyword_fields, filter_fields),
            scroll = '2m'
      )
    
      return await query_retrieve_all_res(es_fields, resp, page_args.size, STANDARD_PAGE_SIZE)
    except Exception:
      message = "Unable to retrieve information for search by keyword"
      return output_error_msg(message)       
  
  
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
                size = STANDARD_PAGE_SIZE,
                query = query,
                scroll = '2m'     
        )
      else:
        message = "Unable to construct query for search by gene operation"
        return output_error_msg(message)       
        
      return await query_retrieve_all_res(es_fields, resp, page_args.size, STANDARD_PAGE_SIZE)
    except Exception:
      message = "Unable to retrieve information for search by gene"
      return output_error_msg(message)       


async def query_return(es_fields, resp):
    """
    Common return function for all queries

    Params: es_fields: List of fields to be returned in elasticsearch query
            resp: Response from elasticsearch query
    """
    results = convert_scroll_hits(es_fields, resp['hits']['hits'])  
    return results


async def query_retrieve_all_res(es_fields: list[str], resp: dict, page_size: int, standard_page_size: int):
    """
    Common return function for all queries

    Params: es_fields: List of fields to be returned in elasticsearch query
            resp: Response from elasticsearch query
    """
    max_num_scroll_requests = page_size // standard_page_size    
    count = 0
    scroll_id = resp['_scroll_id']
    compliant_results = []    

    while len(resp['hits']['hits']):
        for hit in resp['hits']['hits']:
          source = hit['_source']
          values = {clean_field_name(key): value for key, value in source.items()} 
          # values['id']  = hit['_id']
          compliant_results.append(SnpModel(**values))
          
        count += 1          
        if count > max_num_scroll_requests:
            await es.clear_scroll(scroll_id=scroll_id)
            return OutputSnpInfo(success = True, message = "OK", details = compliant_results, version = get_version_info(es_fields)) 
        
        resp = await es.scroll(
            scroll_id = scroll_id,
            scroll = '2s'
        )

        if scroll_id != resp['_scroll_id']:
            print(f'Error retrieving information for scroll id {scroll_id}')
            return output_error_msg("Error retrieving SNP information")
                       
    # count = 0, standard_page_size or no matches for query
    await es.clear_scroll(scroll_id=scroll_id)    
    return OutputSnpInfo(success = True, message = "OK", details = compliant_results, version = get_version_info(es_fields)) 


