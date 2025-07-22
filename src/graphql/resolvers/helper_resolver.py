import inspect
import json
import typing
from typing import Dict
from src.graphql.gene_pos import get_pos_from_gene_id, map_gene, chromosomal_location_dic
from src.graphql.models.snp_model import ScrollSnp, Snp, SnpAggs
from src.graphql.models.annotation_model import AggregationItem, Bucket, DocCount, FilterArgs, Histogram

from src.utils import clean_field_name

def _map_aggs_value(key, value):
        """
        Mapping aggregation values to the correct type

        Params: key: key of the aggregation
                value: values of the aggregation

        Returns: value of the aggregation for the key
        """
        if key.endswith(('min', 'max')):
            return value.get('value')
        elif key.endswith('missing'):
            return DocCount(doc_count=value['doc_count'])
        elif key in ('histogram', 'frequency'):
            return [Bucket(key=b['key'], doc_count=b['doc_count']) for b in value['buckets']]
        else:
            return value.get('doc_count')
          

def convert_hits(hits):
    """
    Converts hits from elasticsearch to Snp objects

    Params: hits: hits from elasticsearch
    
    Returns: List of Snp objects
    """
    compliant_results = []
    for hit in hits:
        source = hit['_source']
        values = {clean_field_name(key): value for key, value in source.items()} 
        values['id']  = hit['_id']
        compliant_results.append(Snp(**values))   
        
    return compliant_results


def convert_scroll_hits(hits, scroll_id=None):
    """
    Converts hits from elasticsearch to ScrollSnp object

    Params: hits: hits from elasticsearch
            scroll_id: scroll_id from elasticsearch
    
    Returns: ScrollSnp object
    """
    compliant_results = []
    for hit in hits:
        source = hit['_source']
        values = {clean_field_name(key): value for key, value in source.items()} 
        values['id']  = hit['_id']
        compliant_results.append(Snp(**values))   
        
    return ScrollSnp(snps=compliant_results, scroll_id=scroll_id)
    
  
def convert_aggs(aggs: Dict) -> SnpAggs: 
    """
    Converts aggregates from elasticsearch to SnpAggs object

    Params: aggs: Dictionary of aggregates from elasticsearch

    Returns: SnpAggs object
    """
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
    """
    Query for getting annotation by chromosome with start and end range of pos

    Params: chr: Chromosome number
            start: Start position
            end: End position
            filter_args: FilterArgs object for field exists filter

    Returns: Query for elasticsearch
    """
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
            if field == 'id':
                field = '_id'
            query["bool"]["filter"].append({"exists": {"field": field}})

    return query


def rsID_query(rsID, filter_args=None):
    """
    Query for getting annotation by rsID

    Params: rsID: rsID of snp
            filter_args: FilterArgs object for field exists filter

    Returns: Query for elasticsearch
    """
    query = {
              "bool": {
                    "filter": [
                      {"term": {"rs_dbSNP151": rsID}},
                    ]
              }
          }
    
    if filter_args and filter_args.exists:
        for field in filter_args.exists:
            if field == 'id':
                field = '_id'
            query["bool"]["filter"].append({"exists": {"field": field}})

    return query


def rsIDs_query(rsIDs, filter_args=None):
    """
    Query for getting annotation by rsIDs

    Params: rsIDs: List of rsIDs of snps
            filter_args: FilterArgs object for field exists filter

    Returns: Query for elasticsearch
    """
    query = {
              "bool": {
                    "filter": [
                      {"terms": {"rs_dbSNP151": rsIDs}}
                    ]
              }
          }

    if filter_args and filter_args.exists:
        for field in filter_args.exists:
            if field == 'id':
                field = '_id'
            query["bool"]["filter"].append({"exists": {"field": field}})

    return query


def IDs_query(ids, filter_args=None):
    """
    Query for getting annotation by IDs

    Params: IDs: List of IDs of snps
            filter_args: FilterArgs object for field exists filter

    Returns: Query for elasticsearch
    """
    query = {
              "bool": {
                 "filter": [
                    {"ids": {"values": ids}}
                 ]
              }
          }
    
    if filter_args and filter_args.exists:
        for field in filter_args.exists:
            if field == 'id':
                field = '_id'
            query["bool"]["filter"].append({"exists": {"field": field}})

    return query


def gene_query(gene, filter_args=None):
    """
    Query for getting annotation by gene product

    Params: gene: Gene product
            filter_args: FilterArgs object for field exists filter

    Returns: Query for elasticsearch
    """
    gene_id = map_gene(gene)
    gene_pos = get_pos_from_gene_id(gene_id, chromosomal_location_dic)

    if gene_pos:
        chr = gene_pos[0]
        start = gene_pos[1]
        end = gene_pos[2]

        query = chromosome_query(chr, start, end, filter_args)
        return query
    
    return None

def keyword_query(keyword: str):
    """
    Query for getting annotation by keyword

    Params: keyword: Keyword for search

    Returns: Query for elasticsearch
    """

    searchable_fields = []
    with open('./data/anno_tree.json') as f:
        data = json.load(f)
        searchable_fields = [elt['name'] for elt in data if elt.get('keyword_searchable', False)]

    query = {
              "multi_match": {
                "query": keyword,
                "fields": searchable_fields
              }
          }

    return query

async def get_aggregation_query(aggregation_fields: list[tuple[str, list[str]]], histogram: Histogram):
    """
    Query for getting aggregates of annotation

    Params: aggregation_fields: List of fields for aggregation, along with their subfields
            histogram: Histogram object for histogram aggregation

    Returns: Query for elasticsearch
    """
    results = dict()
    for field, subfields in aggregation_fields:

        # Check the type of the field. If it is a string, then we have to add .keyword to the field name while querying missing and frequency
        # Using the pydantic model Snp, we can check the type of the field
        is_text_field = typing.get_args(inspect.get_annotations(Snp)[field])[0] == str
        textual_suffix = '.keyword' if is_text_field else ''
             
        for subfield in subfields:
            if subfield == 'doc_count': 
                results[f'{field}_doc_count'] = {
                    "filter" : {
                        "exists": {
                            "field": field
                        }
                    }
                }
                    
            elif subfield == 'min':
                results[f'{field}_min'] = {
                    "min": {
                        "field": field
                    }
                }

            elif subfield == 'max':
                results[f'{field}_max'] = {
                    "max": {
                        "field": field
                    }
                }
            
            elif subfield == 'frequency':
                results[f'{field}_frequency'] = {
                    "terms": {
                        "field": field + textual_suffix,
                        "min_doc_count": 0,
                        "size": 20
                    }
                }

            elif subfield == 'missing':
                results[f'{field}_missing'] = {
                    "missing": {
                        "field": field + textual_suffix
                    }
                }

            elif subfield == 'histogram':
                results[f'{field}_histogram'] = {
                    "histogram": {
                        "field": field,
                        "interval": histogram.interval,
                        "extended_bounds": {
                            "min": histogram.min,
                            "max": histogram.max
                        }
                    }
                }

    return results


def get_default_aggregation_fields(es_fields: list[str]):
    """
    Get default aggregation fields for elasticsearch query

    Params: es_fields: List of fields to be returned in elasticsearch query

    Returns: List of fields for aggregation
    """
    return [(field, ['doc_count']) for field in es_fields]