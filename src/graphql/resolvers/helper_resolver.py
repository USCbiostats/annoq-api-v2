from typing import Dict
from src.graphql.gene_pos import get_pos_from_gene_id, map_gene, chromosomal_location_dic
from src.graphql.models.snp_model import Snp, SnpAggs
from src.graphql.models.annotation_model import AggregationItem, Bucket, DocCount, Histogram

from src.utils import clean_field_name

def _map_aggs_value(key, value):
        if key.endswith(('min', 'max')):
            return value.get('value')
        elif key.endswith('missing'):
            return DocCount(doc_count=value['doc_count'])
        elif key in ('histogram', 'frequency'):
            return [Bucket(key=b['key'], doc_count=b['doc_count']) for b in value['buckets']]
        else:
            return value.get('doc_count')
          

def convert_hits(hits, scroll_id=None):
    compliant_results = []
    for hit in hits:
        source = hit['_source']
        values = {clean_field_name(key): value for key, value in source.items()} 
        values['id']  = hit['_id']
        if scroll_id != None:
            values['scroll_id'] = scroll_id
        compliant_results.append(Snp(**values))   
        
    return compliant_results
  
  
def convert_aggs2(aggs):
    compliant_aggs = {clean_field_name(key): value for key, value in aggs.items()}

    data = {}
    for key, val in compliant_aggs.items():
        data[key] = AggregationItem(doc_count=aggs[key]['doc_count'] if key in aggs else None,
                            min=aggs[f'{key}_min']['value'] if f'{key}_min' in aggs else None,
                            max=aggs[f'{key}_max']['value'] if f'{key}_max' in aggs else None,
                            histogram=[Bucket(key=b['key'], doc_count=b['doc_count']) for b in aggs['histogram']['buckets']] 
                            if 'histogram' in aggs else None,
                            missing=DocCount(doc_count=aggs[f'{key}_missing']['doc_count']) if f'{key}_missing' in aggs else None,
                            frequency=[Bucket(key=b['key'], doc_count=b['doc_count']) for b in aggs[f'{key}_frequency']['buckets']])
                          
                          
    return SnpAggs(**data)
  
  
  
def convert_aggs(aggs: Dict) -> SnpAggs: 

    data = {}

    for key, val in aggs.items():
        key_split = key.split('_')
        prefix = '_'.join(key_split[:-1])
        suffix = key_split[-1]

        if suffix == 'count':
            suffix = 'doc_count'
            prefix_split = prefix.split('_')
            prefix = '_'.join(prefix_split[:-1])

        if prefix not in data:
            data[prefix] = AggregationItem(doc_count=None)

        if hasattr(data[prefix], suffix):
            setattr(data[prefix], suffix, _map_aggs_value(suffix, val))

    return SnpAggs(**data)
  
  

def annotation_query():
    return {"match_all": {}}


def chromosome_query(chr, start, end, filter_args=None):
    query = {
        "bool": {
            "filter": [
                {"term": {"chr": chr}},
                {"range": {"pos": {"gte": start, "lte": end}}}
            ]
        }
    }

    if filter_args and filter_args.exists:
        for field in filter_args.exists:
            query["bool"]["filter"].append({"exists": {"field": field}})

    return query


def rsID_query(rsID, filter_args=None):
    query = {
              "bool": {
                    "filter": [
                      {"term": {"rs_dbSNP151": rsID}},
                    ]
              }
          }
    
    if filter_args and filter_args.exists:
        for field in filter_args.exists:
            query["bool"]["filter"].append({"exists": {"field": field}})

    return query


def rsIDs_query(rsIDs, filter_args=None):
    query = {
              "bool": {
                    "filter": [
                      {"terms": {"rs_dbSNP151": rsIDs}}
                    ]
              }
          }

    if filter_args and filter_args.exists:
        for field in filter_args.exists:
            query["bool"]["filter"].append({"exists": {"field": field}})

    return query


def IDs_query(ids, filter_args=None):
    query = {
              "bool": {
                 "filter": [
                    {"ids": {"values": ids}}
                 ]
              }
          }
    
    if filter_args and filter_args.exists:
        for field in filter_args.exists:
            query["bool"]["filter"].append({"exists": {"field": field}})

    return query


def gene_query(gene, filter_args=None):

    gene_id = map_gene(gene)
    gene_pos = get_pos_from_gene_id(gene_id, chromosomal_location_dic)

    if gene_pos:
        chr = gene_pos[0]
        start = gene_pos[1]
        end = gene_pos[2]

        query = chromosome_query(chr, start, end, filter_args)
        return query
    
    return None

async def get_aggregation_query(es_fields: list[str], histogram: Histogram):
    results = dict()
    for field in es_fields:
        
        results[f'{field}_doc_count'] = {
           "filter" : {
            "exists": {
              "field": field
            }
           }
        }

        results[f'{field}_min'] = {
          "min": {
            "field": "pos"
          }
       }

        results[f'{field}_max'] = {
            "max": {
              "field": "pos"
            }
        }

        results[f'{field}_frequency'] = {
          "terms": {
            "field": "pos",
            "min_doc_count": 0,
            "size": 20
          }
       }

        results[f'{field}_missing'] = {
          "missing": {
              "field": "pos"
            }
       }

        results[f'{field}_histogram'] = {
          "histogram": {
            "field": "pos",
            "interval": histogram.interval,
            "extended_bounds": {
              "min": histogram.min,
              "max": histogram.max
            }
          }
       }

    return results