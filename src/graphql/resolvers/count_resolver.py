from ...config.es import es
from ...config.settings import settings
from ..models.annotation_model import PageArgs
from .helper_resolver import IDs_query, annotation_query, chromosome_query, convert_hits, gene_query, get_aggregation_query, rsID_query, rsIDs_query


async def get_annotations_count():

    resp = await es.count(
          index = settings.ES_INDEX,
          query = annotation_query()
    )
    return resp['count']


async def count_by_chromosome(chr: str, start: int, end: int):

    resp = await es.count(
          index = settings.ES_INDEX,
          query = chromosome_query(chr, start, end),
    )
    return resp['count']


async def count_by_rsID(rsID:str):

    resp = await es.count(
          index = settings.ES_INDEX,
          query = rsID_query(rsID)
    )
    return resp['count']


async def count_by_rsIDs(rsIDs: list[str]):

    resp = await es.count(
          index = settings.ES_INDEX,
          query = rsIDs_query(rsIDs)
    )
    return resp['count']


async def count_by_IDs(ids: list[str]):

    resp = await es.count(
          index = settings.ES_INDEX,
          query = IDs_query(ids)
    )
    return resp['count']


async def count_by_gene(gene:str):
      query = gene_query(gene)

      if query is not None:
        resp = await es.count(
                index = settings.ES_INDEX,
                query = query
        )
        return resp['count']
      
      return 0