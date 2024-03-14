from typing import List, Optional
import strawberry
from strawberry.types import Info
from models.annoq_model import AnnoqDataType
from models.helper_models import PageArgs

from resolvers.resolver import get_annotations, search_by_chromosome, search_by_gene, search_by_rsID, search_by_rsIDs, search_by_IDs
from resolvers.resolver_count import count_by_IDs, count_by_chromosome, count_by_gene, count_by_rsID, count_by_rsIDs, get_annotations_count
from utils import get_selected_fields

@strawberry.type
class Query:
    
    @strawberry.field
    async def GetAnnotations(self, info: Info) -> List[AnnoqDataType]: 
        fields = get_selected_fields(info)
        return await get_annotations(fields)
    
    @strawberry.field
    async def CountAnnotations(self) -> int: 
        return await get_annotations_count()
    
    @strawberry.field
    async def GetSNPsByChromosome(self, info: Info, chr: str, start: int, end: int, 
                                  page_args: Optional[PageArgs] = None) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await search_by_chromosome(fields, chr, start, end, page_args)
    
    @strawberry.field
    async def CountSNPsByChromosome(self, chr: str, start: int, end: int) -> int:
        return await count_by_chromosome(chr, start, end)
    
    @strawberry.field
    async def GetSNPsByRsID(self, info: Info, rsID: str,
                            page_args: Optional[PageArgs] = None) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await search_by_rsID(fields, rsID, page_args)
    
    @strawberry.field
    async def CountSNPsByRsID(self, rsID: str) -> int:
        return await count_by_rsID(rsID)
    
    @strawberry.field
    async def GetSNPsByRsIDs(self, info: Info, rsIDs: list[str],
                             page_args: Optional[PageArgs] = None) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await search_by_rsIDs(fields, rsIDs, page_args)
    
    @strawberry.field
    async def CountSNPsByRsIDs(self, rsIDs: list[str]) -> int:
        return await count_by_rsIDs(rsIDs)
     
    @strawberry.field
    async def GetSNPsByIDs(self, info: Info, ids: list[str],
                          page_args: Optional[PageArgs] = None) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await search_by_IDs(fields, ids, page_args)
    
    @strawberry.field
    async def CountSNPsByIDs(self, ids: list[str]) -> int:
        return await count_by_IDs(ids)
    
    @strawberry.field
    async def GetSNPsByGeneProduct(self, info: Info, gene: int,
                                   page_args: Optional[PageArgs] = None) -> List[AnnoqDataType]:
        fields = get_selected_fields(info)
        return await search_by_gene(fields, gene, page_args)
    
    @strawberry.field
    async def CountSNPsByGeneProduct(self, gene: int) -> int:
        return await count_by_gene(gene)