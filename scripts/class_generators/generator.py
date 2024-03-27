
import asyncio
import json
from elasticsearch import AsyncElasticsearch
import os
from dotenv import load_dotenv
from src.utils import clean_field_name

load_dotenv()


ES_URL:str = os.getenv("ES_URL")
ES_INDEX:str = os.getenv("ES_INDEX")
GENERATED_SCHEMA_DIR = './scripts/class_generators/generated_schemas'
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

es = AsyncElasticsearch(ES_URL,
    connections_per_node=400,
    request_timeout=120,
    max_retries=10,
    retry_on_timeout=True)


async def get_mapping():
    mapping = await es.indices.get_mapping(index = ES_INDEX)
    properties =  mapping[ES_INDEX]['mappings']['properties']
    return properties


def generate_snp_schema(mapping):
    json_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Snp",
        "type": "object",
        "properties": {},
    }
        
    for field, details in mapping.items():
        cleaned_field = clean_field_name(field)
        es_type = details['type']
        json_schema['properties'][cleaned_field] = TYPE_MAPPINGS.get(es_type, {"type": "string"})

    return json_schema


def generate_snp_aggs_schema(mapping):
    json_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "SnpAggs",
        "type": "object",
        "properties": {},
    }
        
    for field, details in mapping.items():
        cleaned_field = clean_field_name(field)
        json_schema['properties'][cleaned_field] = {"type": "model.AggregationItem"}

    return json_schema

        
def write_to_json(data, output_file, indent=None):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=indent)


if __name__ == "__main__":
    
    if not os.path.exists(GENERATED_SCHEMA_DIR):
        os.makedirs(GENERATED_SCHEMA_DIR)
    
    loop = asyncio.get_event_loop()
    mapping = loop.run_until_complete(get_mapping())

    snp_schema = generate_snp_schema(mapping)
    write_to_json(snp_schema, os.path.join(GENERATED_SCHEMA_DIR, 'snp_schema.json'), indent=2)

    snp_aggs_schema = generate_snp_aggs_schema(mapping)
    write_to_json(snp_aggs_schema, os.path.join(GENERATED_SCHEMA_DIR, 'snp_aggs_schema.json'), indent=2)

    loop.run_until_complete(es.close())
    loop.close()