import json
from src.utils import clean_field_name

annotations = []

with open("./data/anno_tree.json") as f:
    data = json.load(f)
    anno_tree = []

    for elt in data:
        if elt["leaf"] == True:
            try:
                name = clean_field_name(elt["name"])
                elt["api_field"] = name
                anno_tree.append(elt)
            except KeyError:
                pass
        else:
            anno_tree.append(elt)


def get_api_field(annotationName):
    for elt in anno_tree:
        if elt["name"] == annotationName:
            return elt["api_field"] if "api_field" in elt else annotationName

    return annotationName


def get_name_from_api_field(api_field):
    for elt in anno_tree:
        if "api_field" in elt and elt["api_field"] == api_field:
            return elt["name"]

    return api_field
