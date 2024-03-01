from typing import List
import strawberry
from strawberry.types import Info
from models.model import AnnoqDataType

from resolvers.resolver import get_annotations, query_by_chromosome, query_by_rsID, query_by_rsIDs
from utils import get_selected_fields

@strawberry.type
class Query:
    
    @strawberry.field
    async def annotations(self, info: Info) -> List[AnnoqDataType]: 
        fields = get_selected_fields(info)
        return await get_annotations(fields)
    
    @strawberry.field
    async def GetSNPsByChromosome(self, info: Info, chr: str, start: int, end: int) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await query_by_chromosome(fields, chr, start, end)
    
    @strawberry.field
    async def GetSNPsByRsID(self, info: Info, rsID: str) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await query_by_rsID(fields, rsID)
    
    @strawberry.field
    async def GetSNPsByRsIDs(self, info: Info, rsIDs: list[str]) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await query_by_rsIDs(fields, rsIDs)
     


