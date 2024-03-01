from itertools import islice
from config.es import es
from config.settings import settings
from models.model import AnnoqSampleData, AnnoqDataType
import re

def to_graphql_name(name):
    if name[0].isdigit():
        return f"x_{name}"
    name = re.sub(r'\([^)]*\)', '', name)
    name = re.sub(r'\/[^\/]*', '', name)
    name = name.replace('-', '_')
    name = name.replace('+', '')
    return name


def convert_hits(hits):
    compliant_results = []
    for hit in hits:
        source = hit['_source']
        compliant_source = {to_graphql_name(key): value for key, value in source.items()}
        compliant_results.append(AnnoqDataType(**compliant_source))
    return compliant_results


# Query for getting all annotations, no filter, size 20
async def get_annotations(es_fields: list[str]):
    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          query = {"match_all": {}},
          size = 20
    )
    results = convert_hits(resp['hits']['hits'])  
    return results

# Query for getting annotation by chromosome with start and end range of pos
async def query_by_chromosome(es_fields: list[str], chr: str, start: int, end: int):
    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          query = {
              "bool": {
                    "must": [
                      {"term": {"chr": chr}},
                      {"range": {"pos": {"gte": start, "lte": end}}}
                    ]
              }
          }
    )
    results = convert_hits(resp['hits']['hits'])    
    return results


async def query_by_rsID(es_fields: list[str], rsID:str):
    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          query = {
              "bool": {
                    "must": [
                      {"term": {"rs_dbSNP151": rsID}},
                    ]
              }
          }
    )
    results = convert_hits(resp['hits']['hits'])    
    return results


async def query_by_rsIDs(es_fields: list[str], rsIDs: list[str]):
    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          query = {
              "bool": {
                    "must": [
                      {"terms": {"rs_dbSNP151": rsIDs}},
                    ]
              }
          }
    )
    results = convert_hits(resp['hits']['hits'])    
    return results