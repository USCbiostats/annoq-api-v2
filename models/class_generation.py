
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


def create_class_schema_from_anno_tree():
    with urllib.request.urlopen("http://annoq.org/api/anno_tree") as url:
        data = json.load(url)

    leaves = [x for x in data['result'] if x['leaf'] == True]
    properties = {}
    types = set()

    for leaf in leaves:
        try:
            name = re.sub(r'\([^)]*\)', '', leaf['name'])
            name = re.sub(r'\/[^\/]*', '', name)
            if name[0].isdigit():
                name = 'x_' + name
            name = name.replace('-', '_')
            name = name.replace('+', '')

            if leaf['field_type'] == 'text':
                properties[name] = {"type": 'string'}

            elif leaf['field_type'] == 'long':
                properties[name] = {"type": 'integer'}

            elif leaf['field_type'] == 'float':
                properties[name] = {"type": 'number', "format": 'float'}

            types.add(leaf['field_type'])

        except KeyError:
           pass

    schema = {
        "title": "AnnoqData",
        "type": "object", 
        "properties": {}
    }

    schema['properties'] = properties
    print('Number of attributes:', len(list(properties.keys())))
    print(types)

    with open("models/class_schema.json", "w") as f:
        json.dump(schema, f)


async def get_mapping():
    mapping = await es.indices.get_mapping(index=ES_INDEX)
    return mapping


def create_class_schema_from_es_mapping():
    mapping = loop.run_until_complete(get_mapping())

    raw_properties = mapping['es_index']['mappings']['properties']

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

            if leaf['type'] == 'text':
                properties[name] = {"type": 'string'}

            elif leaf['type'] == 'long':
                properties[name] = {"type": 'integer'}

            elif leaf['type'] == 'float':
                properties[name] = {"type": 'number', "format": 'float'}

            types.add(leaf['type'])

        except KeyError:
           pass

    schema = {
        "title": "AnnoqData",
        "type": "object", 
        "properties": {}
    }

    schema['properties'] = properties
    print('Number of attributes:', len(list(properties.keys())))
    print(types)

    with open("models/class_schema.json", "w") as f:
        json.dump(schema, f)


loop = asyncio.get_event_loop()
create_class_schema_from_es_mapping()
loop.run_until_complete(es.close())
loop.close()