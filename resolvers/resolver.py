from config.es import es
from config.settings import settings
from models.annoq_model import AnnoqDataType
from models.helper_models import AggregationItem, Bucket, DocCount, Field, Frequency, PageArgs
import re
import requests
from config.settings import settings

def to_graphql_name(name):
    if name[0].isdigit():
        return f"x_{name}"
    name = re.sub(r'\([^)]*\)', '', name)
    name = re.sub(r'\/[^\/]*', '', name)
    name = name.replace('-', '_')
    name = name.replace('+', '')
    return name


def convert_hits(hits, aggregations):
    compliant_results = []
    for hit in hits:
        source = hit['_source']
        compliant_source = {to_graphql_name(key): value for key, value in source.items()}

        data = {}
        for key, val in compliant_source.items():
           data[key] = Field(value=val, aggs=AggregationItem(doc_count=aggregations[key]['doc_count'] if key in aggregations else None,
                              min=aggregations['pos_min']['value'] if 'pos_min' in aggregations else None,
                              max=aggregations['pos_max']['value'] if 'pos_max' in aggregations else None,
                              histogram=[Bucket(key=b['key'], doc_count=b['doc_count']) for b in aggregations['histogram']['buckets']] 
                              if 'histogram' in aggregations else None,
                              missing=DocCount(doc_count=aggregations['pos_missing']['doc_count']) if 'pos_missing' in aggregations else None,
                              frequency=Frequency(doc_count_error_upper_bound=aggregations['pos_frequency']['doc_count_error_upper_bound'],
                                                 sum_other_doc_count=aggregations['pos_frequency']['sum_other_doc_count'],
                                                 buckets=[Bucket(key=b['key'], doc_count=b['doc_count']) for b in aggregations['pos_frequency']['buckets']] 
                                                 if 'pos_frequency' in aggregations else None)))
           
        data['id']  = hit['_id']
            
        compliant_results.append(AnnoqDataType(**data))
    return compliant_results


# Query for getting all annotations, no filter, size 20
async def get_annotations(es_fields: list[str]):
    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          query = {"match_all": {}},
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
          query = {
              "bool": {
                    "must": [
                      {"term": {"chr": chr}},
                      {"range": {"pos": {"gte": start, "lte": end}}}
                    ]
              }
          },
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
          query = {
              "bool": {
                    "must": [
                      {"term": {"rs_dbSNP151": rsID}},
                    ]
              }
          },
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
          query = {
              "bool": {
                    "filter": [
                      {"terms": {"rs_dbSNP151": rsIDs}}
                    ]
              }
          },
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
          query = {
              "bool": {
                 "filter": [
                    {"ids": {"values": ids}}
                 ]
              }
          },
          aggs = await get_aggregation_query(es_fields)
    )
    results = convert_hits(resp['hits']['hits'], resp['aggregations'])    
    return results

# query for gene product
async def search_by_gene(es_fields: list[str], gene:int, page_args=PageArgs):
    if page_args is None:
      page_args = PageArgs
      
    response = requests.get(settings.ANNOTATION_API + '/gene?gene=' + str(gene))

    if response.status_code == 200:

        data = response.json()
        chr = data['gene_info']['contig']
        start = data['gene_info']['start']
        end = data['gene_info']['end']

        resp = await es.search(
                index = settings.ES_INDEX,
                source = es_fields,
                from_= page_args.from_,
                size = page_args.size,
                query = {
                    "bool": {
                        "must": [
                          {"term": {"chr": chr}},
                          {"range": {"pos": {"gte": start, "lte": end}}}
                        ]
                  }
                },
                aggs = await get_aggregation_query(es_fields)
        )
        results = convert_hits(resp['hits']['hits'], resp['aggregations'])    
        return results

    
async def get_aggregation_query(es_fields: list[str]):
    results = dict()
    for field in es_fields:
        
        results[field] = {
           "filter" : {
            "exists": {
              "field": field
            }
           }
        }

    if field == "pos":
       results['pos_min'] = {
          "min": {
            "field": "pos"
          }
       }

       results['pos_max'] = {
            "max": {
              "field": "pos"
            }
        }
       
       results['histogram'] = {
          "histogram": {
            "field": "pos",
            "interval": 4893.27,
            "extended_bounds": {
              "min": 10636,
              "max": 499963
            }
          }
       }

       results['pos_frequency'] = {
          "terms": {
            "field": "pos",
            "min_doc_count": 0,
            "size": 20
          }
       }

       results['pos_missing'] = {
          "missing": {
              "field": "pos"
            }
       }

    return results