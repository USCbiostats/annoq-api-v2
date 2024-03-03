from typing import List, Optional
import strawberry
from strawberry.types import Info
from models.model import AnnoqDataType, PageArgs

from resolvers.resolver import get_annotations, search_by_chromosome, search_by_gene, search_by_rsID, search_by_rsIDs, search_by_ID
from utils import get_selected_fields

@strawberry.type
class Query:
    
    @strawberry.field
    async def annotations(self, info: Info) -> List[AnnoqDataType]: 
        fields = get_selected_fields(info)
        return await get_annotations(fields)
    
    @strawberry.field
    async def GetSNPsByChromosome(self, info: Info, chr: str, start: int, end: int, 
                                  page_args: Optional[PageArgs] = None) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await search_by_chromosome(fields, chr, start, end, page_args)
    
    @strawberry.field
    async def GetSNPsByRsID(self, info: Info, rsID: str) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await search_by_rsID(fields, rsID)
    
    @strawberry.field
    async def GetSNPsByRsIDs(self, info: Info, rsIDs: list[str]) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await search_by_rsIDs(fields, rsIDs)
     
    @strawberry.field
    async def GetSNPsByID(self, info: Info, id: str) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await search_by_ID(fields, id)
    
    @strawberry.field
    async def GetSNPsByGeneProduct(self, info: Info, gene: int) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await search_by_gene(fields, gene)


