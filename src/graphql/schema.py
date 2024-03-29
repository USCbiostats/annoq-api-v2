from typing import List, Optional
import strawberry
from strawberry.types import Info
from src.graphql.models.snp_model import Snp, SnpAggs
from src.graphql.models.annotation_model import PageArgs, QueryType

from src.graphql.resolvers.snp_resolver import get_annotations, search_by_chromosome, search_by_gene, search_by_rsID, search_by_rsIDs, search_by_IDs
from src.graphql.resolvers.count_resolver import count_by_IDs, count_by_chromosome, count_by_gene, count_by_rsID, count_by_rsIDs, get_annotations_count
from src.utils import get_selected_fields

@strawberry.type
class Query:
    
    @strawberry.field
    async def GetAnnotations(self, info: Info) -> List[Snp]: 
        fields = get_selected_fields(info)
        return await get_annotations(fields, QueryType.SNPS)
    
    @strawberry.field
    async def CountAnnotations(self) -> int: 
        return await get_annotations_count()
    
    @strawberry.field
    async def DownloadAnnotations(self, fields: list[str]) -> str: 
        return await get_annotations(fields, QueryType.DOWNLOAD)
    

    @strawberry.field
    async def GetSNPsByChromosome(self, info: Info, chr: str, start: int, end: int,
                                  page_args: Optional[PageArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_chromosome(fields, chr, start, end, QueryType.SNPS, page_args)
    
    @strawberry.field
    async def GetAggsByChromosome(self, info: Info, chr: str, start: int, end: int,
                                  page_args: Optional[PageArgs] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        return await search_by_chromosome(fields, chr, start, end, QueryType.AGGS, page_args)
    
    @strawberry.field
    async def CountSNPsByChromosome(self, chr: str, start: int, end: int) -> int:
        return await count_by_chromosome(chr, start, end)
    
    @strawberry.field
    async def DownloadSNPsByChromosome(self, chr: str, start: int, end: int, fields: list[str],
                                  page_args: Optional[PageArgs] = None) -> str:
        return await search_by_chromosome(fields, chr, start, end, QueryType.DOWNLOAD, page_args)
    

    @strawberry.field
    async def GetSNPsByRsID(self, info: Info, rsID: str,
                            page_args: Optional[PageArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_rsID(fields, rsID, QueryType.SNPS, page_args)
    
    @strawberry.field
    async def GetAggsByRsID(self, info: Info, rsID: str,
                                  page_args: Optional[PageArgs] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        return await search_by_rsID(fields, rsID, QueryType.AGGS, page_args)
    
    @strawberry.field
    async def CountSNPsByRsID(self, rsID: str) -> int:
        return await count_by_rsID(rsID)
    
    @strawberry.field
    async def DownloadSNPsByRsID(self, rsID: str, fields: list[str],
                            page_args: Optional[PageArgs] = None) -> str:
        return await search_by_rsID(fields, rsID, QueryType.DOWNLOAD, page_args)
    

    @strawberry.field
    async def GetSNPsByRsIDs(self, info: Info, rsIDs: list[str],
                             page_args: Optional[PageArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_rsIDs(fields, rsIDs, QueryType.SNPS, page_args)
    
    @strawberry.field
    async def GetAggsByRsIDs(self, info: Info, rsIDs: list[str],
                                  page_args: Optional[PageArgs] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        return await search_by_rsIDs(fields, rsIDs, QueryType.AGGS, page_args)
    
    @strawberry.field
    async def CountSNPsByRsIDs(self, rsIDs: list[str]) -> int:
        return await count_by_rsIDs(rsIDs)
    
    @strawberry.field
    async def DownloadSNPsByRsIDs(self, rsIDs: list[str], fields: list[str],
                             page_args: Optional[PageArgs] = None) -> str:
        return await search_by_rsIDs(fields, rsIDs, QueryType.DOWNLOAD, page_args)
    
     
    @strawberry.field
    async def GetSNPsByIDs(self, info: Info, ids: list[str],
                          page_args: Optional[PageArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_IDs(fields, ids, QueryType.SNPS, page_args)
    
    @strawberry.field
    async def GetAggsByIDs(self, info: Info, ids: list[str],
                                  page_args: Optional[PageArgs] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        return await search_by_IDs(fields, ids, QueryType.AGGS, page_args)
    
    @strawberry.field
    async def CountSNPsByIDs(self, ids: list[str]) -> int:
        return await count_by_IDs(ids)
    
    @strawberry.field
    async def DownloadSNPsByIDs(self, ids: list[str], fields: list[str],
                          page_args: Optional[PageArgs] = None) -> str:
        return await search_by_IDs(fields, ids, QueryType.DOWNLOAD, page_args)
    
    
    @strawberry.field
    async def GetSNPsByGeneProduct(self, info: Info, gene: str,
                                   page_args: Optional[PageArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_gene(fields, gene, QueryType.SNPS, page_args)
    
    @strawberry.field
    async def GetAggsByGeneProduct(self, info: Info, gene: str,
                                  page_args: Optional[PageArgs] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        return await search_by_gene(fields, gene, QueryType.AGGS, page_args)
    
    @strawberry.field
    async def CountSNPsByGeneProduct(self, gene: str) -> int:
        return await count_by_gene(gene)
    
    @strawberry.field
    async def DownloadSNPsByGeneProduct(self, gene: str, fields: list[str],
                                   page_args: Optional[PageArgs] = None) -> str:
        return await search_by_gene(fields, gene, QueryType.DOWNLOAD, page_args)