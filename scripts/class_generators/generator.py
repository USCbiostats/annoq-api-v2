
import asyncio
import urllib.request 
import json
import re
from elasticsearch import AsyncElasticsearch
import os
from dotenv import load_dotenv

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
            name = re.sub(r'\([^)]*\)', '', key)
            name = re.sub(r'\/[^\/]*', '', name)
            if name[0].isdigit():
                name = 'x_' + name
            name = name.replace('-', '_')
            name = name.replace('+', '')

            properties[name] = {"type": "model.Annotation"}

            types.add(leaf['type'])

        except KeyError:
           pass

    schema = {
        "title": "Snps",
        "type": "object", 
        "properties": {}
    }

    schema['properties'] = properties

    with open("models/class_schema.json", "w") as f:
        json.dump(schema, f)


loop = asyncio.get_event_loop()
create_class_schema_from_es_mapping()
loop.run_until_complete(es.close())
loop.close()