
import asyncio
import json
from elasticsearch import AsyncElasticsearch
import os
from dotenv import load_dotenv
from src.utils import clean_field_name

load_dotenv()
ES_URL:str = os.getenv("ES_URL")
ES_INDEX:str = os.getenv("ES_INDEX")

es = AsyncElasticsearch(ES_URL,
    connections_per_node=400,
    request_timeout=120,
    max_retries=10,
    retry_on_timeout=True)


async def get_mapping():
    mapping = await es.indices.get_mapping(index = ES_INDEX)
    return mapping


def create_class_schema_from_es_mapping():
    mapping = loop.run_until_complete(get_mapping())

    raw_properties = mapping[ES_INDEX]['mappings']['properties']

    properties = {}
    types = set()

    for key in raw_properties.keys():
        leaf = raw_properties[key]
        try:
            name = clean_field_name(key)

            properties[name] = {"type": "model.Annotation"}
            types.add(leaf['type'])

        except KeyError:
           pass

    schema = {
        "title": "Snp",
        "type": "object", 
        "properties": {}
    }

    schema['properties'] = properties

    with open("./scripts/class_generators/class_schema.json", "w") as f:
        json.dump(schema, f)


loop = asyncio.get_event_loop()
create_class_schema_from_es_mapping()
loop.run_until_complete(es.close())
loop.close()