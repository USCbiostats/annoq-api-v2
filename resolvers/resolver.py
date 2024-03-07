from config.es import es
from config.settings import settings
from models.model import AnnoqDataType, PageArgs
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


def convert_hits(hits):
    compliant_results = []
    for hit in hits:
        source = hit['_source']
        compliant_source = {to_graphql_name(key): value for key, value in source.items()}
        compliant_source['id']  = hit['_id']
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
async def search_by_chromosome(es_fields: list[str], chr: str, start: int, end: int, page_args=PageArgs):
    if page_args is None:
      page_args = PageArgs

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_ + 1,
          size = page_args.size,
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


async def search_by_rsID(es_fields: list[str], rsID:str, page_args=PageArgs):
    if page_args is None:
      page_args = PageArgs

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_ + 1,
          size = page_args.size,
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


async def search_by_rsIDs(es_fields: list[str], rsIDs: list[str], page_args=PageArgs):
    if page_args is None:
      page_args = PageArgs

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_ + 1,
          size = page_args.size,
          query = {
              "bool": {
                    "filter": [
                      {"terms": {"rs_dbSNP151": rsIDs}}
                    ]
              }
          }
    )
    results = convert_hits(resp['hits']['hits'])    
    return results

# query for VCF file
async def search_by_IDs(es_fields: list[str], ids: list[str], page_args=PageArgs):
    if page_args is None:
      page_args = PageArgs

    resp = await es.search(
          index = settings.ES_INDEX,
          source = es_fields,
          from_= page_args.from_ + 1,
          size = page_args.size,
          query = {
              "bool": {
                 "filter": [
                    {"ids": {"values": ids}}
                 ]
              }
          }
    )
    results = convert_hits(resp['hits']['hits'])    
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
                from_= page_args.from_ + 1,
                size = page_args.size,
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
    
    
async def get_aggregation(es_fields: list[str], fields:list[str], page_args=PageArgs):
    return None