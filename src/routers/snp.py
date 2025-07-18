"""snp router."""
import logging
from enum import Enum
from typing import List
from fastapi import APIRouter, Path, Query
import json
from src.graphql.models.annotation_model import FilterArgs, PageArgs
from src.graphql.resolvers.api_snp_resolver import  output_error_msg, search_by_chromosome, search_by_rsIDs, search_by_IDs, search_by_keyword, search_by_gene
from src.graphql.resolvers.api_count_resolver import count_by_chromosome, count_by_rsIDs, count_by_keyword
from src.graphql.models.return_info_model import OutputSnpInfo, OutputCountInfo
from src.data_adapter.snp_attributes import get_gene_search_fields, get_snp_attrib_json, get_attrib_list

# Constants
MAX_PAGE_SIZE =  50 #1000000

MAX_ATTRIB_SIZE = 20;    

CHR_1 = "1"
CHR_2 = "2"
CHR_3 = "3"
CHR_4 = "4"
CHR_5 = "5"
CHR_6 = "6"
CHR_7 = "7"
CHR_8 = "8"
CHR_9 = "9"
CHR_10 = "10"
CHR_11 = "11"
CHR_12= "12"
CHR_13 = "13"
CHR_14 = "14"
CHR_15 = "15"
CHR_16 = "16"
CHR_17 = "17"
CHR_18 = "18"
CHR_19 = "19"
CHR_20 = "20"
CHR_21 = "21"
CHR_22 = "22"
CHR_X = "X"

class ChromosomeIdentifierType(str, Enum):
    CHR_1 = CHR_1
    CHR_2 = CHR_2
    CHR_3 = CHR_3
    CHR_4 = CHR_4
    CHR_5 = CHR_5                
    CHR_6 = CHR_6
    CHR_7 = CHR_7
    CHR_8 = CHR_8
    CHR_9 = CHR_9
    CHR_10 = CHR_10 
    CHR_11 = CHR_11
    CHR_12 = CHR_12
    CHR_13 = CHR_13
    CHR_14 = CHR_14
    CHR_15 = CHR_15                
    CHR_16 = CHR_16
    CHR_17 = CHR_17
    CHR_18 = CHR_18
    CHR_19 = CHR_19
    CHR_20 = CHR_20
    CHR_21 = CHR_21
    CHR_22 = CHR_22
    CHR_X = CHR_X
    
    
TITLE = "AnnoQ API"

    
SUMMARY = "API for accessing SNP data from Annoq.org"

DESCRIPTION = """
API for programatic access of SNP data from Annoq.org

### ATTRIBUTES

Retrieve information about the SNP attributes available for each SNP in the system

### SNP

Retrieve SNPs based on: 
1.  Chromosome and position range
2.  RSID list
3.  Gene

### Count
Retrieve number of SNP's matching following search criteria:
1.  Chromosome and position range
2.  RSID list
3.  Gene
"""

VERSION = "2.5"
    
TAGS_METADATA = [
    {
    "name": "ATTRIBUTES",
    "description": "Retrieves Information about SNP attributes",
    },
    {
    "name": "SNP",
    "description": "Retrieves SNP's based on search criteria.  Note, in addition to requested SNP attributes, the system will also return the unique identifier for the SNP"
    },
    {
    "name": "Count",
    "description": "Retrieves the count of SNP's that match the search criteria"
    },
]



def parse_annoq_config(config_str:str):
    try:
        json_object = json.loads(config_str)
        attribs = json_object["_source"]
        supported_attribs = []
        for attrib in attribs:
            if attrib in get_attrib_list():
                supported_attribs.append(attrib)
        if len(supported_attribs) > MAX_ATTRIB_SIZE:
            return "Maximum number of requested 'fields' should not exceed " + str(MAX_ATTRIB_SIZE)
        if len(supported_attribs) == 0:
            return "No valid SNP attributes selected for output"
        return supported_attribs
    except json.JSONDecodeError:
        return "Error parsing SNP attribute information"
    
def parse_filter_fields(filter_string:str):
    if filter_string:
        filter_fields = filter_string.split(",")
        supported_fields = []
        for field in filter_fields:
            if field in get_attrib_list():
                supported_fields.append(field)
        if len(supported_fields) == 0:
            return None
        return supported_fields         
    else:
        return None        
    
    
router = APIRouter()
@router.post("/fastapi/snpAttributes",
            tags=["ATTRIBUTES"],
            description="Returns available list of SNP attributes.  Each entry has detailed information about the attribute such as the label to be used for quering the API, the name of the attribute used by Annoq.org website, a description of the attribute, the version of data and if the attribute can be used for searching by keyword")
async def get_snp_attributes():
    return get_snp_attrib_json()
    


@router.post("/fastapi/snp/chr",
            tags=["SNP"],
            description="Search by chromosome id and position range.  The following have to be specified: The chromosome number (or 'X' for the X-chromosome), the chromosome start and stop region positions and the SNP attributes.  The pagination start and stop range and list of filter fields are optional.",
            response_model=OutputSnpInfo,
            response_model_exclude_none=True)
async def get_snps_by_chr(
    chromosome_identifier: ChromosomeIdentifierType = Query(
        deault=ChromosomeIdentifierType.CHR_1,
        description="Chromosome id to search."
    ),
    start_position: int = Query(1, description="Start position region of search"),  
    end_position: int = Query(100000, description="End position region of search"),
    fields: str = Query(default='{"_source":["Basic Info","chr","pos","ref","alt","rs_dbSNP151"]}', 
        description="Contents of SNP configuration file generated from selected SNP attributes and downloaded from annoq.org.  The maximum number of attributes should not exceed " + str(MAX_ATTRIB_SIZE)),
    pagination_from: int = Query(default=None, example=0, description="starting index for pagination"),
    pagination_size: int = Query(default = None, example=50, description="Number of results per page.  Maximum is " + str(MAX_PAGE_SIZE), le = MAX_PAGE_SIZE),
    filter_fields: str = Query(default=None,
        description="SNP attribute labels (columns) that should not be empty for the record to be retrieved.  These are delimited by comma ','.  Example ANNOVAR_ucsc_Transcript_ID,VEP_ensembl_Gene_ID,SnpEff_ensembl_CDS_position_CDS_len,flanking_0_GO_biological_process_complete_list_id,flanking_0_GO_cellular_component_complete_list_id")
    ):
    
    page_args = PageArgs(from_=pagination_from, size=pagination_size)
    if filter_fields is not None:
        filter_list = parse_filter_fields(filter_fields)
        if filter_list is not None:
            filter_args = FilterArgs(exists=filter_list)
        else:
         filter_args = None   
    else:
        filter_args = None
    
    attribs = parse_annoq_config(fields)
    if type(attribs) is str:
        return output_error_msg(message=attribs)

    return await search_by_chromosome(attribs, chromosome_identifier.value,  start_position, end_position, page_args, filter_args)


@router.post("/fastapi/snp/rsidList",
            tags=["SNP"],
            description="Search for specified list of RSIDs.  The following have to be specified: One or more RSIDs and the SNP attributes.  The pagination start and stop range and list of filter fields are optional.",
            response_model=OutputSnpInfo,
            response_model_exclude_none=True)
async def get_snps_by_rsidList(
    rsid_list: str = Query(default="rs1219648,rs2912774,rs2981582,rs1101006,rs1224211,rs1076148,rs2116830,rs1801516,rs2250417,rs1436109,rs1227926,rs1047964,rs900145,rs4757144,rs6486122,rs4627050,rs6578985,rs2074238,rs179429,rs231362,rs231906,rs108961,rs7481311", 
        description="List of RSIDS to search.  Delimited by comma ','.  Example rs574852966,rs148600903"),
    fields: str = Query(default='{"_source":["Basic Info","chr","pos","ref","alt","rs_dbSNP151"]}', 
        description="Contents of SNP configuration file generated from selected SNP attributes and downloaded from annoq.org.  The maximum number of attributes should not exceed " + str(MAX_ATTRIB_SIZE)),  
    pagination_from: int = Query(default=None, example=0, description="starting index for pagination"),
    pagination_size: int = Query(default = None, example=50, description="Number of results per page.  Maximum is " + str(MAX_PAGE_SIZE), le = MAX_PAGE_SIZE),
    filter_fields: str = Query(default=None,
        description="SNP attribute labels (columns) that should not be empty for the record to be retrieved.  These are delimited by comma ','.  Example ANNOVAR_ucsc_Transcript_ID,VEP_ensembl_Gene_ID,SnpEff_ensembl_CDS_position_CDS_len,flanking_0_GO_biological_process_complete_list_id,flanking_0_GO_cellular_component_complete_list_id")
    ):

    page_args = PageArgs(from_=pagination_from, size=pagination_size)
    if filter_fields is not None:
        filter_list = parse_filter_fields(filter_fields)
        if filter_list is not None:
            filter_args = FilterArgs(exists=filter_list)
        else:
         filter_args = None   
    else:
        filter_args = None

    rsIDs = rsid_list.split(",")    
    attribs = parse_annoq_config(fields)
    if type(attribs) is str:
        return output_error_msg(message=attribs)
        
    return await search_by_rsIDs(attribs, rsIDs, page_args, filter_args)



# @router.post("/fastapi/snp/idList",
#             tags=["SNP"],
#             description="Search for specified list of ID's.  This is a unique identifier for each SNP in the system.  It is a concatenation of the chromosome, followed by a colon (':'), followed by the position, followed by the reference nucleotide, followed by a greater than symbol ('>') followed by alternate nucleotide.  The following have to be specified: One or more IDs and the SNP attributes.  The pagination start and stop range and list of filter fields are optional.",
#             response_model=OutputSnpInfo,
#             response_model_exclude_none=True)
# async def get_snps_by_idList(
#     id_list: str = Query(default="1:115921355T>C,1:12046063G>T,12:13641706C>A", 
#         description="List of IDS to search.  Delimited by comma ','.  Example 20:60309G>T,20:65497T>G"),
#     fields: str = Query(default='{"_source":["Basic Info","chr","pos","ref","alt","rs_dbSNP151"]}', 
#         description="Contents of SNP configuration file generated from selected SNP attributes and downloaded from annoq.org"),    
#     pagination_from: int = Query(default=None, example=0, description="starting index for pagination"),
#     pagination_size: int = Query(default = None, example=50, description="Number of results per page.  Maximum is " + str(MAX_PAGE_SIZE), le = MAX_PAGE_SIZE),
#     filter_fields: str = Query(default=None,
#         description="SNP attribute labels (columns) that should not be empty for the record to be retrieved.  These are delimited by comma ','.  Example ANNOVAR_ensembl_Closest_gene(intergenic_only),SnpEff_ensembl_CDS_position_CDS_len,flanking_0_GO_biological_process_complete_list_id,flanking_0_GO_cellular_component_complete_list_id")
#     ):

#     page_args = PageArgs(from_=pagination_from, size=pagination_size)
#     if filter_fields is not None:
#         filter_args = FilterArgs(exists=filter_fields.split(","))
#     else:
#         filter_args = None

#     idList = id_list.split(",")    
#     try:
#         json_object = json.loads(fields)
#         attribs = json_object["_source"] 
#     except json.JSONDecodeError:
#         return output_error_msg("Unable to retrieve information")
        
#     return await search_by_IDs(attribs, idList, page_args, filter_args)



# @router.post("/fastapi/snp/keyword",
#             tags=["SNP"],
#             description="Search for specified keyword.  The following have to be specified: The SNP attribute information to retrieve.  The pagination start and stop range and are optional.",
#             response_model=OutputSnpInfo,
#             response_model_exclude_none=True)
# async def get_snps_by_keyword(
#     keyword: str = Query(default="Signaling by GPCR", 
#         description="keyword of phrase to search"),
#     fields: str = Query(default='{"_source":["Basic Info","chr","pos","ref","alt","rs_dbSNP151"]}', 
#         description="Contents of SNP configuration file generated from selected SNP attributes and downloaded from annoq.org.  The maximum number of attributes should not exceed " + str(MAX_ATTRIB_SIZE)),
#     pagination_from: int = Query(default=None, example=0, description="starting index for pagination"),
#     pagination_size: int = Query(default = None, example=50, description="Number of results per page.  Maximum is " + str(MAX_PAGE_SIZE), le = MAX_PAGE_SIZE),
#     ):

#     page_args = PageArgs(from_=pagination_from, size=pagination_size)


#     try:
#         json_object = json.loads(fields)
#         attribs = json_object["_source"]
#         if len(attribs) > MAX_ATTRIB_SIZE:
#             return output_error_msg(message="Maximum number of requested 'fields' should not exceed " + str(MAX_ATTRIB_SIZE))         
#     except json.JSONDecodeError:
#         return output_error_msg("Unable to retrieve information")
        
#     return await search_by_keyword(attribs, keyword, page_args)



@router.post("/fastapi/snp/gene",
            tags=["SNP"],
            description="Search for specified gene product.  The following have to be specified: A gene Id and  the SNP attributes.  The pagination start and stop range and list of filter fields are optional.",
            response_model=OutputSnpInfo,
            response_model_exclude_none=True)
async def get_snps_by_gene(
    gene: str = Query(default="ZMYND11", 
        description="Gene id to search"),
    fields: str = Query(default='{"_source":["Basic Info","chr","pos","ref","alt","rs_dbSNP151"]}', 
        description="Contents of SNP configuration file generated from selected SNP attributes and downloaded from annoq.org.  The maximum number of attributes should not exceed " + str(MAX_ATTRIB_SIZE)),   
    pagination_from: int = Query(default=None, example=0, description="starting index for pagination"),
    pagination_size: int = Query(default = None, example=50, description="Number of results per page.  Maximum is " + str(MAX_PAGE_SIZE), le = MAX_PAGE_SIZE),
    filter_fields: str = Query(default=None,
        description="SNP attribute labels (columns) that should not be empty for the record to be retrieved.  These are delimited by comma ','.  Example ANNOVAR_ucsc_Transcript_ID,VEP_ensembl_Gene_ID,SnpEff_ensembl_CDS_position_CDS_len,flanking_0_GO_biological_process_complete_list_id,flanking_0_GO_cellular_component_complete_list_id")
    ):

    page_args = PageArgs(from_=pagination_from, size=pagination_size)
    filter_list = parse_filter_fields(filter_fields)
    
    keyword_fields = get_gene_search_fields()   
    attribs = parse_annoq_config(fields)
    if type(attribs) is str:
        return output_error_msg(message=attribs)      
        
    return await search_by_keyword(attribs, gene, page_args, keyword_fields, filter_list)


@router.post("/fastapi/count/chr",
            tags=["Count"],
            description="Returns number of SNP records based on specified chromosome, start position, end position and filter arguments",
            response_model=OutputCountInfo)
async def count_snps_by_chromosome(
    chromosome_identifier: ChromosomeIdentifierType = Query(
        deault=ChromosomeIdentifierType.CHR_1,
        description="The chromosome number (or 'X' for the X-chromosome)"
    ),
    start_position: int = Query(1, description="Start position region of search"),  
    end_position: int = Query(100000, description="End position region of search"),
    filter_fields: str = Query(default=None,
        description="SNP attribute labels (columns) that should not be empty for the record to be retrieved.  These are delimited by comma ','.  Example ANNOVAR_ucsc_Transcript_ID,VEP_ensembl_Gene_ID,SnpEff_ensembl_CDS_position_CDS_len,flanking_0_GO_biological_process_complete_list_id,flanking_0_GO_cellular_component_complete_list_id")
    ):
    if filter_fields is not None:
        filter_list = parse_filter_fields(filter_fields)
        if filter_list is not None:
            filter_args = FilterArgs(exists=filter_list)
        else:
         filter_args = None   
    else:
        filter_args = None  
    return await count_by_chromosome(chromosome_identifier.value,  start_position, end_position, filter_args)


@router.post("/fastapi/count/rsidList",
            tags=["Count"],
            description="Returns the number of SNPs defined in the system that have matching RSID's from the specified list of RSIDs.",
            response_model=OutputCountInfo)
async def count_snps_by_rsidList(
    rsid_list: str = Query(default="rs1219648,rs2912774,rs2981582,rs1101006,rs1224211,rs1076148,rs2116830,rs1801516,rs2250417,rs1436109,rs1227926,rs1047964,rs900145,rs4757144,rs6486122,rs4627050,rs6578985,rs2074238,rs179429,rs231362,rs231906,rs108961,rs7481311", 
        description="List of RSIDS to search.  Delimited by comma ','.  Example rs574852966,rs148600903"),
    filter_fields: str = Query(default=None,
        description="SNP attribute labels (columns) that should not be empty for the record to be retrieved.  These are delimited by comma ','.  Example ANNOVAR_ucsc_Transcript_ID,VEP_ensembl_Gene_ID,SnpEff_ensembl_CDS_position_CDS_len,flanking_0_GO_biological_process_complete_list_id,flanking_0_GO_cellular_component_complete_list_id")
    ):
    rsIDs = rsid_list.split(",")      
    if filter_fields is not None:
        filter_list = parse_filter_fields(filter_fields)
        if filter_list is not None:
            filter_args = FilterArgs(exists=filter_list)
        else:
         filter_args = None   
    else:
        filter_args = None   
    return await count_by_rsIDs(rsIDs, filter_args)
    

# @router.post("/fastapi/count/idList",
#             tags=["Count"],
#             description="Returns the number of SNPs defined in the system that have matching ID's from the specified list of IDs.",
#             response_model=OutputCountInfo)
# async def count_snps_by_idList(
#     id_list: str = Query(default="1:115921355T>C,1:12046063G>T,12:13641706C>A", 
#         description="List of IDS to search.  Delimited by comma ','.  Example 20:60309G>T,20:65497T>G"),
#     filter_fields: str = Query(default=None,
#         description="SNP attribute labels (columns) that should not be empty for the record to be retrieved.  These are to be delimited by comma ','.  Example \"ANNOVAR_ensembl_Closest_gene(intergenic_only),SnpEff_ensembl_CDS_position_CDS_len,flanking_0_GO_biological_process_complete_list_id,flanking_0_GO_cellular_component_complete_list_id")
#     ):
#     idList = id_list.split(",")      
#     if filter_fields is not None:
#         filter_args = FilterArgs(exists=filter_fields.split(","))
#     else:
#         filter_args = None    
#     return await count_by_IDs(idList, filter_args)
 
 
# @router.post("/fastapi/count/keyword",
#             tags=["Count"],
#             description="Returns the number of SNPs defined in the system that have been associated with the keyword",
#             response_model=OutputCountInfo)
# async def count_snps_by_keyword(
#     keyword: str = Query(default="Signaling by GPCR", 
#         description="keyword of phrase to search")
#     ):
 
#     return await count_by_keyword(keyword)



@router.post("/fastapi/count/gene",
            tags=["Count"],
            description="Returns the number of SNPs defined in the system that have been associated for the specified gene product.  The following have to be specified: The gene id and the SNP attributes.  The filter fields are optional.",
            response_model=OutputCountInfo)
async def count_snps_by_gene(
    gene: str = Query(default="abca1", 
        description="Gene product to search"),
    filter_fields: str = Query(default=None,
        description="SNP attribute labels (columns) that should not be empty for the record to be retrieved.  These are delimited by comma ','.  Example ANNOVAR_ucsc_Transcript_ID,VEP_ensembl_Gene_ID,SnpEff_ensembl_CDS_position_CDS_len,flanking_0_GO_biological_process_complete_list_id,flanking_0_GO_cellular_component_complete_list_id")
    ):

    filter_list = parse_filter_fields(filter_fields)
        
    keyword_fields = get_gene_search_fields()         
    return await count_by_keyword(gene, keyword_fields, filter_list)
        