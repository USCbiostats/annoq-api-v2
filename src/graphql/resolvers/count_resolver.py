from ...config.es import es
from ...config.settings import settings
from src.graphql.models.annotation_model import FilterArgs, PageArgs
from .helper_resolver import IDs_query, annotation_query, chromosome_query, convert_hits, gene_query, get_aggregation_query, rsID_query, rsIDs_query


async def get_annotations_count():

    resp = await es.count(
          index = settings.ES_INDEX,
          query = annotation_query()
    )
    return resp['count']


async def count_by_chromosome(chr: str, start: int, end: int, filter_args=FilterArgs):

    resp = await es.count(
          index = settings.ES_INDEX,
          query = chromosome_query(chr, start, end, filter_args),
    )
    return resp['count']


async def count_by_rsID(rsID:str, filter_args=FilterArgs):

    resp = await es.count(
          index = settings.ES_INDEX,
          query = rsID_query(rsID, filter_args)
    )
    return resp['count']


async def count_by_rsIDs(rsIDs: list[str], filter_args=FilterArgs):

    resp = await es.count(
          index = settings.ES_INDEX,
          query = rsIDs_query(rsIDs, filter_args)
    )
    return resp['count']


async def count_by_IDs(ids: list[str], filter_args=FilterArgs):

    resp = await es.count(
          index = settings.ES_INDEX,
          query = IDs_query(ids, filter_args)
    )
    return resp['count']


async def count_by_gene(gene:str, filter_args=FilterArgs):
      query = gene_query(gene, filter_args)

      if query is not None:
        resp = await es.count(
                index = settings.ES_INDEX,
                query = query
        )
        return resp['count']
      
      return 0