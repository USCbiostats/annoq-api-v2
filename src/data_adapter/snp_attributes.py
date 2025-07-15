import json
import copy
from src.utils import clean_field_name


class SnpAttributes:
    def __init__(self):
        self.leaf_attrib_list = None
        self.searchable_list = None
        self.detail_lookup = None
        self.leaf_name_lookup = None
        
        
    def initialize(self):   
        with open('./data/anno_tree.json') as f:
            data = json.load(f)
            attrib_list = []
            searchable_list = []
            detail_lookup = {}
            leaf_name_lookup = {}
            
            for elt in data:
                if 'id' in elt:
                    detail_info =  copy.deepcopy(elt)
                    detail_lookup[elt['id']] = detail_info
                    #If no version information, get from parent
                    if detail_info.get('version') is None and 'parent_id' in detail_info and detail_info['parent_id'] in detail_lookup:
                        parent = detail_lookup[detail_info['parent_id']]
                        if 'version' in parent:
                            detail_info['version'] = parent['version']
                            
                            
                if elt['leaf'] == True:
                    cur = {}
                    name = clean_field_name(elt['name'])
                    searchable = False
                    if 'keyword_searchable' in elt:
                        searchable = bool (elt['keyword_searchable'])
                    cur["api_label"] =  name
                    if 'label' in elt:
                        cur['display_label'] = elt['label']
                    else:
                        cur['display_label'] = name    
                    cur["searchable"] = searchable
                    if searchable == True:
                        searchable_list.append(name)
                    # if 'label' in elt:
                    #     cur["display_label"] = elt['label']
                    if 'detail' in elt:
                        cur["definition"] = elt['detail']
                    if 'field_type' in elt:
                        cur["data_type"] = elt['field_type']    
                    attrib_list.append(cur)
                    if 'id' in elt:
                        leaf_name_lookup[name] = elt['id']
                        if  elt['id'] in detail_lookup: 
                            details = detail_lookup[elt['id']]
                            if 'version' in details:
                                cur["version"]  = details['version']
                        
                       
        self.attrib_list = attrib_list
        self.searchable_list = searchable_list
        self.detail_lookup = detail_lookup
        self.leaf_name_lookup = leaf_name_lookup       
        


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


def get_version_info(fields):
    rtn_lookup = {}
    for field in fields:
        if field in snpAttributes.leaf_name_lookup:
            id = snpAttributes.leaf_name_lookup[field]
            if id in snpAttributes.detail_lookup:
                details = snpAttributes.detail_lookup[id]
                if 'version' in details:
                    rtn_lookup[field] = details['version']
    return str(rtn_lookup)       