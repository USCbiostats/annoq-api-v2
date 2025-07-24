# from __future__ import annotations
# from typing import Optional
# from pydantic import BaseModel, Field
import json
import copy
from src.utils import clean_field_name





# class MyModel(BaseModel):
#     id: Optional[str] = None
#     field_A: Optional[int] = Field(None, alias='_A')
#     field_B: Optional[int] = Field(None, alias='_B')
#     field_C: Optional[int] = Field(None, alias='_C')

#     model_config = {
#         "populate_by_name": True  # Whether an aliased field may be populated by its name as given by the model attribute, as well as the alias. Defaults to False
#     }

# # Input using aliases
# some_json = {"_B": 1234, "_C": 5678}
# an_instance = MyModel(**some_json)

# print(an_instance)



GENE_SEARCH_COLS = ["ANNOVAR_ensembl_Closest_gene(intergenic_only)","ANNOVAR_ensembl_Gene_ID","ANNOVAR_refseq_Gene_ID","ANNOVAR_refseq_Closest_gene(intergenic_only)","SnpEff_ensembl_Gene_ID","SnpEff_refseq_Gene_ID","VEP_ensembl_Gene_ID","VEP_refseq_Gene_ID","enhancer_linked_genes"]


class SnpAttributes:
    def __init__(self):
        self.leaf_attrib_list = None
        self.searchable_set = None
        self.detail_lookup = None
        self.leaf_name_lookup = None
        self.leaf_set = None
        self.gene_search_fields = None
        self.cleaned_to_actual_label_lookup = None
        self.leaf_name_to_type = None
        
        
    def initialize(self):   
        with open('./data/anno_tree.json') as f:
            data = json.load(f)
            leaf_attrib_list = []
            searchable_set = set()
            detail_lookup = {}
            leaf_name_lookup = {}
            cleaned_to_actual_label_lookup = {}
            leaf_name_to_type = {}
            gene_search_fields = []
            
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
                    # name = clean_field_name(elt['name'])
                    cleaned_to_actual_label_lookup[clean_field_name(elt['name'])] = elt['name']
                    
                    searchable = False
                    if 'keyword_searchable' in elt:
                        searchable = bool (elt['keyword_searchable'])
                    cur["api_label"] =  elt['name']
                    if 'label' in elt:
                        cur['display_label'] = elt['label']
                    else:
                        cur['display_label'] = elt['name']    
                    # cur["searchable"] = searchable
                    if searchable == True:
                        searchable_set.add(elt['name'])
                    # if 'label' in elt:
                    #     cur["display_label"] = elt['label']
                    if 'detail' in elt:
                        cur["definition"] = elt['detail']
                    if 'field_type' in elt:
                        cur["data_type"] = elt['field_type']
                        leaf_name_to_type[elt['name']] = elt['field_type']
                    leaf_attrib_list.append(cur)
                    
                    #Get list of api_labels and also propagate version information from parent to child
                    if 'id' in elt:
                        leaf_name_lookup[elt['name']] = elt['id']
                        if  elt['id'] in detail_lookup: 
                            details = detail_lookup[elt['id']]
                            if 'version' in details:
                                cur["version"]  = details['version']
                        


            for gene_col in GENE_SEARCH_COLS:
                if gene_col in searchable_set:
                    gene_search_fields.append(gene_col)
                else:
                    print(f'Gene search string not found for {gene_col}')
                       
        self.leaf_attrib_list = leaf_attrib_list
        self.searchable_set = searchable_set
        self.detail_lookup = detail_lookup
        self.leaf_name_lookup = leaf_name_lookup
        self.leaf_set = set(leaf_name_lookup.keys())
        self.gene_search_fields = gene_search_fields
        self.cleaned_to_actual_label_lookup = cleaned_to_actual_label_lookup
        self.leaf_name_to_type = leaf_name_to_type
              
        


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
    return  {"results": snpAttributes.leaf_attrib_list}

def get_keyword_searchable_set():
    return snpAttributes.searchable_set


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

def get_gene_search_fields(): 
    return snpAttributes.gene_search_fields

def get_attrib_list():
    return snpAttributes.leaf_set


def get_cleaned_to_actual_label_lookup():
    return snpAttributes.cleaned_to_actual_label_lookup

def get_name_to_type():
    return snpAttributes.leaf_name_to_type




           