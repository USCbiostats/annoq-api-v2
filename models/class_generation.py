
import urllib.request 
import json
import re
from config.es import es
from config.settings import settings
import asyncio 

async def get_mapping():
    mapping = await es.indices.get_mapping(index=settings.ES_INDEX)
    return mapping


def create_class_schema():
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
