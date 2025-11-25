
import asyncio
import copy
import json
from elasticsearch import AsyncElasticsearch
import os
from src.utils import clean_field_name
from src.config.settings import settings

ES_URL:str = settings.ES_URL
ES_INDEX:str = settings.ES_INDEX
GENERATED_SCHEMA_DIR = './scripts/class_generators/generated_schemas'
GENERATED_MODEL_DIR = './src/graphql/models/generated/'
TYPE_MAPPINGS = {
    "long": {"type": "integer", "format": "int64"},
    "integer": {"type": "integer", "format": "int32"},
    "short": {"type": "integer", "format": "int16"},
    "byte": {"type": "integer", "format": "int8"},
    "double": {"type": "number", "format": "double"},
    "float": {"type": "number", "format": "float"},
    "date": {"type": "string", "format": "date-time"},
    "boolean": {"type": "boolean"},
    "keyword": {"type": "string"},
    "text": {"type": "string"},
    "object": {"type": "object"},
}

def init_snp_dict():
    with open('./data/anno_tree.json') as f:
        data = json.load(f)
        snp_dict = {}
        for elt in data:
            if elt['leaf'] == True:
                cur = {}
                name = clean_field_name(elt['name'])
                searchable = False
                if 'keyword_searchable' in elt:
                    searchable = bool (elt['keyword_searchable'])
                cur["api_label"] =  elt['name']
                cur["searchable"] = searchable
                if 'label' in elt:
                    cur["display_label"] = elt['label']
                if 'detail' in elt:
                    cur["definition"] = elt['detail']
                snp_dict[name] = cur
        return snp_dict



snp_attrib_dict = init_snp_dict()  

es = AsyncElasticsearch(ES_URL,
    connections_per_node=400,
    request_timeout=120,
    max_retries=10,
    retry_on_timeout=True)


async def get_mapping():
    """
    Get mappings from elasticsearch index

    Returns properties of mappings
    """
    mapping = await es.indices.get_mapping(index = ES_INDEX)
    properties =  mapping[ES_INDEX]['mappings']['properties']
    return properties


def generate_snp_schema(mapping):
    """
    Generates the schema for the SnpModel from elasticsearch mappings

    Params: mapping: elasticsearch mappings

    Returns: SnpModel schema
    """
    json_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "SnpModel",
        "type": "object",
        "properties": {},
    }
    
    json_schema['properties']['id'] = {"type": "string"}
    for field, details in mapping.items():
        cleaned_field = clean_field_name(field)
        es_type = details['type']
        cur = copy.deepcopy(TYPE_MAPPINGS.get(es_type, {"type": "string"}))
        if cleaned_field in snp_attrib_dict:
            other_details = snp_attrib_dict[cleaned_field] 
            cur["description"] = other_details.get("definition", None)
        else:
            cur["description"] = None
        cur["title"] = other_details.get("api_label")    
        json_schema['properties'][cleaned_field] = cur
            
    return json_schema


def generate_snp_aggs_schema(mapping):
    """
    Generates the schema for the SnpAggsModel from elasticsearch mappings

    Params: mapping: elasticsearch mappings

    Returns: SnpAggsModel schema
    """
    json_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "SnpAggsModel",
        "type": "object",
        "properties": {},
    }
        
    for field, details in mapping.items():
        cleaned_field = clean_field_name(field)
        json_schema['properties'][cleaned_field] = {"type": "model.AggregationItem"}

    return json_schema

        
def write_to_json(data, output_file, indent=None):
    """
    Writes data to a json file
    
    Params: data: data to write to file
            output_file: file to write to
            indent: indentation level
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=indent)


if __name__ == "__main__":
    
    if not os.path.exists(GENERATED_SCHEMA_DIR):
        os.makedirs(GENERATED_SCHEMA_DIR)
        
    if not os.path.exists(GENERATED_MODEL_DIR):
        os.makedirs(GENERATED_MODEL_DIR)    
    
    loop = asyncio.get_event_loop()
    mapping = loop.run_until_complete(get_mapping())

    snp_schema = generate_snp_schema(mapping)
    write_to_json(snp_schema, os.path.join(GENERATED_SCHEMA_DIR, 'snp_schema.json'), indent=2)

    snp_aggs_schema = generate_snp_aggs_schema(mapping)
    write_to_json(snp_aggs_schema, os.path.join(GENERATED_SCHEMA_DIR, 'snp_aggs_schema.json'), indent=2)

    loop.run_until_complete(es.close())
    loop.close()