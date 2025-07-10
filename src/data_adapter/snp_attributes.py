import json
from src.utils import clean_field_name


class SnpAttributes:
    def __init__(self):
        self.leaf_attrib_list = None
        self.searchable_list = None
        
        
    def initialize(self):   
        with open('./data/anno_tree.json') as f:
            data = json.load(f)
            attrib_list = []
            searchable_list = []
            for elt in data:
                if elt['leaf'] == True:
                    cur = {}
                    name = clean_field_name(elt['name'])
                    searchable = False
                    if 'keyword_searchable' in elt:
                        searchable = bool (elt['keyword_searchable'])
                    cur["api_label"] =  name
                    if 'label' in elt:
                        cur["name"] = elt['label']
                    else:
                        cur["name"] = name    
                    cur["searchable"] = searchable
                    if searchable == True:
                        searchable_list.append(name)
                    if 'label' in elt:
                        cur["display_label"] = elt['label']
                    if 'detail' in elt:
                        cur["definition"] = elt['detail']
                    attrib_list.append(cur)
        self.attrib_list = attrib_list
        self.searchable_list = searchable_list         
        


# def init_snp_attribute_info():
#     with open('./data/anno_tree.json') as f:
#         data = json.load(f)
#         attrib_list = []
#         for elt in data:
#             if elt['leaf'] == True:
#                 cur = {}
#                 name = clean_field_name(elt['name'])
#                 searchable = False
#                 if 'keyword_searchable' in elt:
#                     searchable = bool (elt['keyword_searchable'])
#                 cur["api_label"] =  name
#                 cur["keyword_searchable"] = searchable
#                 if 'label' in elt:
#                     cur["display_label"] = elt['label']
#                 if 'detail' in elt:
#                     cur["definition"] = elt['detail']
#                 attrib_list.append(cur)             
#         return attrib_list
    
    
# snp_attrib_list = init_snp_attribute_info()

# def get_snp_attrib_json():
#     return  {"results": snp_attrib_list}



snpAttributes = SnpAttributes()
snpAttributes.initialize()


def get_snp_attrib_json():
    return  {"results": snpAttributes.attrib_list}

def get_keyword_searchable_fields():
    return snpAttributes.searchable_list
                