from src.config.es import es
from src.config.settings import settings
from src.graphql.models.annotation_model import FilterArgs, PageArgs
from src.graphql.resolvers.helper_resolver import IDs_query, chromosome_query, rsIDs_query, gene_query
from src.data_access_object.keyword_search import keyword_query
from src.graphql.models.return_info_model import OutputCountInfo
#from src.graphql.resolvers.api_snp_helper_resolver import output_error_msg, convert_scroll_hits

async def count_by_chromosome(chr: str, start: int, end: int, filter_args=FilterArgs):
      """ 
      Query for getting count of annotation by chromosome with start and end range of pos

      Params: es_fields: List of fields to be returned in elasticsearch query
            chr: Chromosome number
            start: Start position
            end: End position
            filter_args: FilterArgs object for field exists filter

      Returns: integer for count of annotations
      """
      try:
        resp = await es.count(
                index = settings.ES_INDEX,
                query = chromosome_query(chr, start, end, filter_args),
        )
        return OutputCountInfo(success = False, message = "OK", details =  resp['count'])
      except Exception:
        return output_error_msg("Unable to retrieve count information for search by chromosome")
    

async def count_by_rsIDs(rsIDs: list[str], filter_args=FilterArgs):
      """ 
      Query for getting count of annotation by rsIDs

      Params: es_fields: List of fields to be returned in elasticsearch query
            rsIDs: List of rsIDs of snps
            filter_args: FilterArgs object for field exists filter

      Returns: integer for count of annotations
      """
      try:
        resp = await es.count(
                index = settings.ES_INDEX,
                query = rsIDs_query(rsIDs, filter_args)
        )
        return OutputCountInfo(success = True, message = "OK", details =  resp['count'])
      except Exception:
        return output_error_msg("Unable to retrieve count information for search by RSID list")
    
    
async def count_by_IDs(ids: list[str], filter_args=FilterArgs):
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
        return output_error_msg("Unable to retrieve count information for search by ID list")    


async def count_by_keyword(keyword: str):
      """ 
      Query for getting count of annotation by keyword

      Params: 
            keyword: Keyword to search

      Returns: integer for count of annotations
      """
      try:
        resp = await es.count(
                index = settings.ES_INDEX,
                query = keyword_query(keyword)
        )
        return OutputCountInfo(success = True, message = "OK", details =  resp['count'])
      except Exception:
        return output_error_msg("Unable to retrieve count information for search by keyword")  


async def count_by_gene(gene:str, filter_args=FilterArgs):
      """ 
      Query for getting count of annotation by rsIDs

      Params: es_fields: List of fields to be returned in elasticsearch query
            gene: Gene product
            filter_args: FilterArgs object for field exists filter

      Returns: integer for count of annotations
      """
      
      try: 
        query = gene_query(gene, filter_args)

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
    
    
    