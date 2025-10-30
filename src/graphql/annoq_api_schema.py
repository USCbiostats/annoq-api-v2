from typing import Optional
import strawberry
from strawberry.types import Info
# from src.graphql.models.snp_model import SnpList

from src.graphql.models.snp_model import ScrollSnp
from src.graphql.models.annotation_model import QueryType
from src.graphql.resolvers.snp_resolver import search_by_chromosome

from src.graphql.models.annotation_model import FilterArgs, PageArgs
from src.graphql.models.return_info_model import OutputSnpInfo
from src.graphql.resolvers.api_snp_resolver import  search_by_chromosome, search_by_rsIDs, search_by_IDs
from src.graphql.resolvers.count_resolver import count_by_chromosome, count_by_rsIDs, count_by_IDs
from src.utils import get_sub_selected_fields

@strawberry.type
class AnnoqApiQuery:
    
    @strawberry.field (
        description="Returns the number of SNPs defined in the system for the specified chromosome and within the start and end position."        
    )
    async def count_SNPs_by_chromosome(self, chr: str, start: int, end: int, filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_chromosome(chr, start, end, filter_args)    


    @strawberry.field(
        description="Returns a list of records where each record has requested SNP attributes.   The following have to be specified: The chromosome number (or 'X' for the X-chromosome), the chromosome start and stop region positions, the SNP attributes to return.  The pagination start and stop range and list of filter fields are optional."
    )
    async def get_SNPs_by_chromosome(self, info: Info, chr: str, start: int, end: int, 
                                  page_args: Optional[PageArgs] = None,
                                  filter_args: Optional[FilterArgs] = None) -> OutputSnpInfo:
        fields = get_sub_selected_fields(info)
        return await search_by_chromosome(fields, chr, start, end, page_args, filter_args)
    
    @strawberry.field(
        description="Testing parameter"
    )
    async def testing_get_SNPs_by_chromosome(self, info: Info, chr: str, start: int, end: int, 
                                  page_args: Optional[PageArgs] = None,
                                  filter_args: Optional[FilterArgs] = None)  -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        return await search_by_chromosome(fields, chr, start, end, QueryType.SCROLL, None, page_args, filter_args)

    
    @strawberry.field(
        description="Returns the number of SNPs defined in the system that have matching RSID's from the specified list of RSIDs."        
    )
    async def count_SNPs_by_RsIDs(self, rsIDs: list[str], filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_rsIDs(rsIDs, filter_args)
    
    @strawberry.field
    async def get_SNPs_by_RsIDs(self, info: Info, rsIDs: list[str], 
                             page_args: Optional[PageArgs] = None,
                             filter_args: Optional[FilterArgs] = None) -> OutputSnpInfo:
        fields = get_sub_selected_fields(info)

        return await search_by_rsIDs(fields, rsIDs, page_args, filter_args)
       
    @strawberry.field(
        description="Returns the number of SNPs defined in the system for the specified IDs"        
    )
    async def count_SNPs_by_IDs(self, ids: list[str], filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_IDs(ids, filter_args)

    
    @strawberry.field
    async def get_SNPs_by_IDs(self, info: Info, ids: list[str], 
                          page_args: Optional[PageArgs] = None,
                          filter_args: Optional[FilterArgs] = None) -> OutputSnpInfo:
        fields = get_sub_selected_fields(info)
        return await search_by_IDs(fields, ids, page_args, filter_args)


