from src.graphql.gene_pos import get_pos_from_gene_id, map_gene, chromosomal_location_dic
from src.graphql.models.snp_model import SnpsType
from src.graphql.models.annotation_model import AggregationItem, Bucket, DocCount, Annotation
import re

from utils import clean_field_name

def convert_hits(hits, aggregations):
    compliant_results = []
    for hit in hits:
        source = hit['_source']
        compliant_source = {clean_field_name(key): value for key, value in source.items()}

        data = {}

        if aggregations is not None:
            for key, val in compliant_source.items():
                data[key] = Annotation(value=val, aggs=AggregationItem(doc_count=aggregations[key]['doc_count'] if key in aggregations else None,
                                    min=aggregations[f'{key}_min']['value'] if f'{key}_min' in aggregations else None,
                                    max=aggregations[f'{key}_max']['value'] if f'{key}_max' in aggregations else None,
                                    histogram=[Bucket(key=b['key'], doc_count=b['doc_count']) for b in aggregations['histogram']['buckets']] 
                                    if 'histogram' in aggregations else None,
                                    missing=DocCount(doc_count=aggregations[f'{key}_missing']['doc_count']) if f'{key}_missing' in aggregations else None,
                                    frequency=[Bucket(key=b['key'], doc_count=b['doc_count']) for b in aggregations[f'{key}_frequency']['buckets']]))
        else:
            for key, val in compliant_source.items():
                data[key] = Annotation(value=val)
           
        data['id']  = hit['_id']
            
        compliant_results.append(SnpsType(**data))
    return compliant_results

def annotation_query():
    return {"match_all": {}}


def chromosome_query(chr, start, end):
    return {
              "bool": {
                    "must": [
                      {"term": {"chr": chr}},
                      {"range": {"pos": {"gte": start, "lte": end}}}
                    ]
              }
    }


def rsID_query(rsID):
    return {
              "bool": {
                    "must": [
                      {"term": {"rs_dbSNP151": rsID}},
                    ]
              }
          }


def rsIDs_query(rsIDs):
    return {
              "bool": {
                    "filter": [
                      {"terms": {"rs_dbSNP151": rsIDs}}
                    ]
              }
          }


def IDs_query(ids):
    return {
              "bool": {
                 "filter": [
                    {"ids": {"values": ids}}
                 ]
              }
          }

def gene_query(gene):

    gene_id = map_gene(gene)
    gene_pos = get_pos_from_gene_id(gene_id, chromosomal_location_dic)

    if gene_pos:
        chr = gene_pos[0]
        start = gene_pos[1]
        end = gene_pos[2]

        query = chromosome_query(chr, start, end)
        return query
    
    return None

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

        results['histogram'] = {
          "histogram": {
            "field": "pos",
            "interval": 50000,
            "extended_bounds": {
              "min": 0,
              "max": 500000
            }
          }
       }

    return results