from ...config.es import es
from ...config.settings import settings
from src.graphql.models.annotation_model import FilterArgs
from .helper_resolver import IDs_query, annotation_query, chromosome_query, gene_query, keyword_query, rsID_query, rsIDs_query
from src.data_access_object.keyword_search import keyword_query_for_fields_with_filters


async def get_annotations_count():
      """ 
      Query for count of annotations

      Returns: integer for count of annotations
      """
      resp = await es.count(
            index = settings.ES_INDEX,
            query = annotation_query()
      )
      return resp['count']


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
      resp = await es.count(
            index = settings.ES_INDEX,
            query = chromosome_query(chr, start, end, filter_args),
      )
      return resp['count']


async def count_by_rsID(rsID:str, filter_args=FilterArgs):
      """ 
      Query for getting count of annotation by rsID

      Params: es_fields: List of fields to be returned in elasticsearch query
            rsID: rsID of snp
            filter_args: FilterArgs object for field exists filter

      Returns: integer for count of annotations
      """
      resp = await es.count(
            index = settings.ES_INDEX,
            query = rsID_query(rsID, filter_args)
      )
      return resp['count']


async def count_by_rsIDs(rsIDs: list[str], filter_args=FilterArgs):
      """ 
      Query for getting count of annotation by rsIDs

      Params: es_fields: List of fields to be returned in elasticsearch query
            rsIDs: List of rsIDs of snps
            filter_args: FilterArgs object for field exists filter

      Returns: integer for count of annotations
      """
      resp = await es.count(
            index = settings.ES_INDEX,
            query = rsIDs_query(rsIDs, filter_args)
      )
      return resp['count']


async def count_by_IDs(ids: list[str], filter_args=FilterArgs):
      """ 
      Query for getting count of annotation by IDs

      Params: es_fields: List of fields to be returned in elasticsearch query
            IDs: List of IDs of snps
            filter_args: FilterArgs object for field exists filter

      Returns: integer for count of annotations
      """
      resp = await es.count(
            index = settings.ES_INDEX,
            query = IDs_query(ids, filter_args)
      )
      return resp['count']


async def count_by_gene(gene:str, filter_args=FilterArgs):
      """ 
      Query for getting count of annotation by rsIDs

      Params: es_fields: List of fields to be returned in elasticsearch query
            gene: Gene product
            filter_args: FilterArgs object for field exists filter

      Returns: integer for count of annotations
      """
      query = gene_query(gene, filter_args)

      if query is not None:
        resp = await es.count(
                index = settings.ES_INDEX,
                query = query
        )
        return resp['count']
      
      return 0

async def count_by_keyword_on_specific_fields(keyword: str, keyword_fields: list[str] = None, filter_args:FilterArgs = None):
      """ 
      Query for getting count of annotation by keyword

      Params: es_fields: List of fields to be returned in elasticsearch query
      keyword: keyword to search
      keyword_fields: list of columns to search
      filter_args: FilterArgs object for field exists filter

      Returns: integer for count of annotations
      """      
      filter_fields = []  
      if filter_args and filter_args.exists:
            for field in filter_args.exists:
                  filter_fields.append(field)  
                  
      resp = await es.count(
            index = settings.ES_INDEX,
            query = keyword_query_for_fields_with_filters(keyword, keyword_fields, filter_fields)
      )
      return resp['count']              

async def count_by_keyword(keyword: str):
      """ 
      Query for getting count of annotation by keyword

      Params: 
            keyword: Keyword to search

      Returns: integer for count of annotations
      """
      resp = await es.count(
            index = settings.ES_INDEX,
            query = keyword_query(keyword)
      )
      return resp['count']