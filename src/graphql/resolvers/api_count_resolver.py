from src.config.es import es
from src.config.settings import settings
from src.graphql.models.annotation_model import FilterArgs, PageArgs
from src.graphql.resolvers.helper_resolver import IDs_query, chromosome_query, rsIDs_query, gene_query
from src.data_access_object.keyword_search import keyword_query_for_fields_with_filters
from src.graphql.models.return_info_model import OutputCountInfo
#from src.graphql.resolvers.api_snp_helper_resolver import output_error_msg, convert_scroll_hits

async def count_by_chromosome(chr: str, start: int, end: int, filter_args: FilterArgs | None = None, search_hrc=None):
      """
      Query for getting count of annotation by chromosome with start and end range of pos

      Params: es_fields: List of fields to be returned in elasticsearch query
            chr: Chromosome number
            start: Start position
            end: End position
            filter_args: FilterArgs object for field exists filter
            search_hrc: When set, restrict to the HRC subset using hg19 fields

      Returns: integer for count of annotations
      """
      try:
        resp = await es.count(
                index = settings.ES_INDEX,
                query = chromosome_query(chr, start, end, filter_args, search_hrc),
        )
        return OutputCountInfo(success = False, message = "OK", details =  resp['count'])
      except Exception:
            message = "Unable to retrieve count information for search by chromosome"
            return output_error_msg(message)
    

async def count_by_rsIDs(rsIDs: list[str], filter_args: FilterArgs | None = None, search_hrc=None):
      """
      Query for getting count of annotation by rsIDs

      Params: es_fields: List of fields to be returned in elasticsearch query
            rsIDs: List of rsIDs of snps
            filter_args: FilterArgs object for field exists filter
            search_hrc: When set, restrict results to the HRC-mapped subset (Mapped_in_HRC=Y), in hg19 space

      Returns: integer for count of annotations
      """
      try:
        resp = await es.count(
                index = settings.ES_INDEX,
                query = rsIDs_query(rsIDs, filter_args, search_hrc)
        )
        return OutputCountInfo(success = True, message = "OK", details =  resp['count'])
      except Exception:
            message = "Unable to retrieve count information for search by RSID list"
            return output_error_msg(message)


async def count_by_IDs(ids: list[str], filter_args: FilterArgs | None = None):
      """ 
      Query for getting count of annotation by IDs

      Params: es_fields: List of fields to be returned in elasticsearch query
            IDs: List of IDs of snps
            filter_args: FilterArgs object for field exists filter

      Returns: integer for count of annotations
      """
      try:      
        resp = await es.count(
                index = settings.ES_INDEX,
                query = IDs_query(ids, filter_args)
        )   
        return OutputCountInfo(success = True, message = "OK", details =  resp['count'])
      except Exception:
            message = "Unable to retrieve count information for search by ID list"
            return output_error_msg(message)    


async def count_by_keyword(keyword: str, keyword_fields: list[str] = None, filter_fields:list[str] = None):
      """ 
      Query for getting count of annotation by keyword

      Params: 
            keyword: Keyword to search

      Returns: integer for count of annotations
      """
      try:
        resp = await es.count(
                index = settings.ES_INDEX,
                query = keyword_query_for_fields_with_filters(keyword, keyword_fields, filter_fields)
        )
        return OutputCountInfo(success = True, message = "OK", details =  resp['count'])
      except Exception:
        message = "Unable to retrieve count information for search by keyword"    
        return output_error_msg(message)  


async def count_by_gene_product(gene:str, filter_args: FilterArgs | None = None, search_hrc=None):
      """
      Query for getting count of annotation by rsIDs

      Params: es_fields: List of fields to be returned in elasticsearch query
            gene: Gene product
            filter_args: FilterArgs object for field exists filter
            search_hrc: When set, resolve hg19 coordinates and restrict to the HRC subset

      Returns: integer for count of annotations
      """

      try:
        query = gene_query(gene, filter_args, search_hrc)

        if query is not None:
            resp = await es.count(
                    index = settings.ES_INDEX,
                    query = query
            )
            return OutputCountInfo(success = True, message = "OK", details =  resp['count'])
        else:
            return output_error_msg("Unable to construct query for counting by gene")      
      except Exception:
        return output_error_msg("Unable to retrieve count information for search by gene")  
  
  
  
  
      




    
    
    
def output_error_msg(message):
    return OutputCountInfo(success = False, message = message, details =  -1)    
    
    
    