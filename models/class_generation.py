
import urllib.request 
import json
import re


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
    # print(schema)

    # schema = {
    #     "title": "Person",
    #     "type": "object",
    #     "properties": {
    #         "name": {
    #             "type": "string"
    #         },
    #         "age": {
    #             "type": "integer"
    #         },
    #         "occupation": {
    #             "type": "string"
    #         }
    #     }
    # }

    with open("models/class_schema.json", "w") as f:
        json.dump(schema, f)
    