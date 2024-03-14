from config.es import es
from config.settings import settings
from models.helper_models import PageArgs
from resolvers.resolver_helper import IDs_query, annotation_query, chromosome_query, convert_hits, gene_query, get_aggregation_query, rsID_query, rsIDs_query


# Query for getting all annotations, no filter, size 20
async def get_annotations(es_fields: list[str]):
    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          query = annotation_query(),
          aggs = await get_aggregation_query(es_fields),
          size = 20
    )
    results = convert_hits(resp['hits']['hits'], resp['aggregations'])  
    return results


# Query for getting annotation by chromosome with start and end range of pos
async def search_by_chromosome(es_fields: list[str], chr: str, start: int, end: int, page_args=PageArgs):
    if page_args is None:
      page_args = PageArgs

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_,
          size = page_args.size,
          query = chromosome_query(chr, start, end),
          aggs = await get_aggregation_query(es_fields)
    )
    results = convert_hits(resp['hits']['hits'], resp['aggregations']) 
    return results


async def search_by_rsID(es_fields: list[str], rsID:str, page_args=PageArgs):
    if page_args is None:
      page_args = PageArgs

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_,
          size = page_args.size,
          query = rsID_query(rsID),
          aggs = await get_aggregation_query(es_fields)
    )
    results = convert_hits(resp['hits']['hits'], resp['aggregations'])    
    return results


async def search_by_rsIDs(es_fields: list[str], rsIDs: list[str], page_args=PageArgs):
    if page_args is None:
      page_args = PageArgs

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_,
          size = page_args.size,
          query = rsIDs_query(rsIDs),
          aggs = await get_aggregation_query(es_fields)
    )
    results = convert_hits(resp['hits']['hits'], resp['aggregations'])    
    return results


# query for VCF file
async def search_by_IDs(es_fields: list[str], ids: list[str], page_args=PageArgs):
    if page_args is None:
      page_args = PageArgs

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_,
          size = page_args.size,
          query = IDs_query(ids),
          aggs = await get_aggregation_query(es_fields)
    )
    results = convert_hits(resp['hits']['hits'], resp['aggregations'])    
    return results


# query for gene product
async def search_by_gene(es_fields: list[str], gene:str, page_args=PageArgs):
    if page_args is None:
      page_args = PageArgs

      query = gene_query(gene)

      if query is not None:
        resp = await es.search(
                index = settings.ES_INDEX,
                source = es_fields,
                from_= page_args.from_,
                size = page_args.size,
                query = query,
                aggs = await get_aggregation_query(es_fields)
        )
        results = convert_hits(resp['hits']['hits'], resp['aggregations'])    
        return results