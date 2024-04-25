from typing import List, Optional
import strawberry
from strawberry.types import Info
from src.graphql.models.snp_model import ScrollSnp, Snp, SnpAggs
from src.graphql.models.annotation_model import FilterArgs, Histogram, PageArgs, QueryType

from src.graphql.resolvers.snp_resolver import get_annotations, scroll_annotations, scroll_by_IDs, scroll_by_chromosome, scroll_by_rsID, scroll_by_rsIDs, search_by_chromosome, search_by_gene, search_by_rsID, search_by_rsIDs, search_by_IDs
from src.graphql.resolvers.count_resolver import count_by_IDs, count_by_chromosome, count_by_gene, count_by_rsID, count_by_rsIDs, get_annotations_count
from src.utils import get_selected_fields, get_sub_selected_fields

@strawberry.type
class Query:
    
    @strawberry.field
    async def GetAnnotations(self, info: Info) -> List[Snp]:
        """Get all annotations""" 
        fields = get_selected_fields(info)
        return await get_annotations(fields, QueryType.SNPS)
    
    @strawberry.field
    async def CountAnnotations(self) -> int: 
        return await get_annotations_count()
    
    @strawberry.field
    async def DownloadAnnotations(self, fields: list[str]) -> str: 
        return await get_annotations(fields, QueryType.DOWNLOAD)
    
    @strawberry.field
    async def ScrollAnnotations(self, info: Info, scroll_id: Optional[str] = None) -> ScrollSnp: 
        fields = get_sub_selected_fields(info)
        return await scroll_annotations(fields, scroll_id)
    

    @strawberry.field
    async def GetSNPsByChromosome(self, info: Info, chr: str, start: int, end: int,
                                  page_args: Optional[PageArgs] = None,
                                  filter_args: Optional[FilterArgs] = None) -> List[Snp]:
        
        fields = get_selected_fields(info)
        return await search_by_chromosome(fields, chr, start, end, QueryType.SNPS, page_args, filter_args)
    
    @strawberry.field
    async def GetAggsByChromosome(self, info: Info, chr: str, start: int, end: int,
                                  page_args: Optional[PageArgs] = None, histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_chromosome(fields, chr, start, end, QueryType.AGGS, page_args, None, histogram)
    
    @strawberry.field
    async def CountSNPsByChromosome(self, chr: str, start: int, end: int, filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_chromosome(chr, start, end, filter_args)
    
    @strawberry.field
    async def DownloadSNPsByChromosome(self, chr: str, start: int, end: int, fields: list[str],
                                  page_args: Optional[PageArgs] = None) -> str:
        return await search_by_chromosome(fields, chr, start, end, QueryType.DOWNLOAD, page_args) 
    
    @strawberry.field
    async def ScrollSNPsByChromosome(self, info: Info, chr: str, start: int, end: int, scroll_id: Optional[str] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        return await scroll_by_chromosome(fields, chr, start, end, scroll_id)
    

    @strawberry.field
    async def GetSNPsByRsID(self, info: Info, rsID: str,
                            page_args: Optional[PageArgs] = None,
                            filter_args: Optional[FilterArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_rsID(fields, rsID, QueryType.SNPS, page_args, filter_args)
    
    @strawberry.field
    async def GetAggsByRsID(self, info: Info, rsID: str,
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_rsID(fields, rsID, QueryType.AGGS, page_args, histogram)
    
    @strawberry.field
    async def CountSNPsByRsID(self, rsID: str, filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_rsID(rsID, filter_args)
    
    @strawberry.field
    async def DownloadSNPsByRsID(self, rsID: str, fields: list[str],
                            page_args: Optional[PageArgs] = None) -> str:
        return await search_by_rsID(fields, rsID, QueryType.DOWNLOAD, page_args)
    
    @strawberry.field
    async def ScrollSNPsByRsID(self, info: Info, rsID: str, scroll_id: Optional[str] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        return await scroll_by_rsID(fields, rsID, scroll_id)
    

    @strawberry.field
    async def GetSNPsByRsIDs(self, info: Info, rsIDs: list[str],
                             page_args: Optional[PageArgs] = None,
                             filter_args: Optional[FilterArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_rsIDs(fields, rsIDs, QueryType.SNPS, page_args, filter_args)
    
    @strawberry.field
    async def GetAggsByRsIDs(self, info: Info, rsIDs: list[str],
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_rsIDs(fields, rsIDs, QueryType.AGGS, page_args, histogram)
    
    @strawberry.field
    async def CountSNPsByRsIDs(self, rsIDs: list[str], filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_rsIDs(rsIDs, filter_args)
    
    @strawberry.field
    async def DownloadSNPsByRsIDs(self, rsIDs: list[str], fields: list[str],
                             page_args: Optional[PageArgs] = None) -> str:
        return await search_by_rsIDs(fields, rsIDs, QueryType.DOWNLOAD, page_args)
    
    @strawberry.field
    async def ScrollSNPsByRsIDs(self, info: Info, rsIDs: list[str], scroll_id: Optional[str] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        return await scroll_by_rsIDs(fields, rsIDs, scroll_id)
    
     
    @strawberry.field
    async def GetSNPsByIDs(self, info: Info, ids: list[str],
                          page_args: Optional[PageArgs] = None,
                          filter_args: Optional[FilterArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_IDs(fields, ids, QueryType.SNPS, page_args, filter_args)
    
    @strawberry.field
    async def GetAggsByIDs(self, info: Info, ids: list[str],
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_IDs(fields, ids, QueryType.AGGS, page_args, None, histogram)
    
    @strawberry.field
    async def CountSNPsByIDs(self, ids: list[str], filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_IDs(ids, filter_args)
    
    @strawberry.field
    async def DownloadSNPsByIDs(self, ids: list[str], fields: list[str],
                          page_args: Optional[PageArgs] = None) -> str:
        return await search_by_IDs(fields, ids, QueryType.DOWNLOAD, page_args)
    
    @strawberry.field
    async def ScrollSNPsByIDs(self, info:Info, ids: list[str], scroll_id: Optional[str] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        return await scroll_by_IDs(fields, ids, scroll_id)
    
    
    @strawberry.field
    async def GetSNPsByGeneProduct(self, info: Info, gene: str,
                                   page_args: Optional[PageArgs] = None,
                                   filter_args: Optional[FilterArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_gene(fields, gene, QueryType.SNPS, page_args, filter_args)
    
    @strawberry.field
    async def GetAggsByGeneProduct(self, info: Info, gene: str,
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_gene(fields, gene, QueryType.AGGS, page_args, None, histogram)
    
    @strawberry.field
    async def CountSNPsByGeneProduct(self, gene: str, filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_gene(gene, filter_args)
    
    @strawberry.field
    async def DownloadSNPsByGeneProduct(self, gene: str, fields: list[str],
                                   page_args: Optional[PageArgs] = None) -> str:
        return await search_by_gene(fields, gene, QueryType.DOWNLOAD, page_args)