
import asyncio
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

annotation_mapping = {}


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
            original = key
            name = re.sub(r'\([^)]*\)', '', key)
            name = re.sub(r'\/[^\/]*', '', name)
            if name[0].isdigit():
                name = '_' + name
            name = name.replace('-', '_')
            name = name.replace('+', '')

            properties[name] = {"type": "model.Annotation"}

            types.add(leaf['type'])
            annotation_mapping[original] = name

        except KeyError:
           pass

    schema = {
        "title": "Snps",
        "type": "object", 
        "properties": {}
    }

    schema['properties'] = properties

    with open("./scripts/class_generators/class_schema.json", "w") as f:
        json.dump(schema, f)


loop = asyncio.get_event_loop()
create_class_schema_from_es_mapping()
json.dump(annotation_mapping, open("./data/annotation_mapping.json", "w"))
loop.run_until_complete(es.close())
loop.close()