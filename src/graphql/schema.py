from typing import List, Optional
import strawberry
from strawberry.types import Info
from src.graphql.models.snp_model import ScrollSnp, Snp, SnpAggs
from src.graphql.models.annotation_model import FilterArgs, Histogram, PageArgs, QueryType, QueryTypeOption

from src.graphql.resolvers.snp_resolver import get_annotations, scroll_annotations_, search_by_chromosome, search_by_gene, search_by_rsID, search_by_rsIDs, search_by_IDs
from src.graphql.resolvers.count_resolver import count_by_IDs, count_by_chromosome, count_by_gene, count_by_rsID, count_by_rsIDs, get_annotations_count
from src.utils import get_selected_fields, get_sub_selected_fields

@strawberry.type
class Query:
    
    @strawberry.field
    async def annotations(self, info: Info) -> List[Snp]:
        fields = get_selected_fields(info)
        return await get_annotations(fields, QueryType.SNPS)
    
    @strawberry.field
    async def count_annotations(self) -> int: 
        return await get_annotations_count()
    
    @strawberry.field
    async def download_annotations(self, fields: list[str]) -> str: 
        return await get_annotations(fields, QueryType.DOWNLOAD)
    
    @strawberry.field
    async def scroll_annotations(self, info: Info, scroll_id: Optional[str] = None) -> ScrollSnp: 
        fields = get_sub_selected_fields(info)
        return await scroll_annotations_(fields, scroll_id)
    

    @strawberry.field
    async def get_SNPs_by_chromosome(self, info: Info, chr: str, start: int, end: int, query_type_option: QueryTypeOption,
                                  page_args: Optional[PageArgs] = None,
                                  filter_args: Optional[FilterArgs] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        if query_type_option == QueryTypeOption.SNPS:
            query_type = QueryType.SNPS
        else:
            query_type = QueryType.SCROLL
        return await search_by_chromosome(fields, chr, start, end, query_type, page_args, filter_args)
    
    @strawberry.field
    async def get_aggs_by_chromosome(self, info: Info, chr: str, start: int, end: int,
                                  page_args: Optional[PageArgs] = None, histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_chromosome(fields, chr, start, end, QueryType.AGGS, page_args, None, histogram)
    
    @strawberry.field
    async def count_SNPs_by_chromosome(self, chr: str, start: int, end: int, filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_chromosome(chr, start, end, filter_args)
    
    @strawberry.field
    async def download_SNPs_by_chromosome(self, chr: str, start: int, end: int, fields: list[str],
                                  page_args: Optional[PageArgs] = None) -> str:
        return await search_by_chromosome(fields, chr, start, end, QueryType.DOWNLOAD, page_args) 
    

    @strawberry.field
    async def get_SNPs_by_RsID(self, info: Info, rsID: str, query_type_option: QueryTypeOption,
                            page_args: Optional[PageArgs] = None,
                            filter_args: Optional[FilterArgs] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        if query_type_option == QueryTypeOption.SNPS:
            query_type = QueryType.SNPS
        else:
            query_type = QueryType.SCROLL
        return await search_by_rsID(fields, rsID, query_type, page_args, filter_args)
    
    @strawberry.field
    async def get_aggs_by_RsID(self, info: Info, rsID: str,
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_rsID(fields, rsID, QueryType.AGGS, page_args, None, histogram)
    
    @strawberry.field
    async def count_SNPs_by_RsID(self, rsID: str, filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_rsID(rsID, filter_args)
    
    @strawberry.field
    async def download_SNPs_by_RsID(self, rsID: str, fields: list[str],
                            page_args: Optional[PageArgs] = None) -> str:
        return await search_by_rsID(fields, rsID, QueryType.DOWNLOAD, page_args)
    

    @strawberry.field
    async def get_SNPs_by_RsIDs(self, info: Info, rsIDs: list[str],
                             page_args: Optional[PageArgs] = None,
                             filter_args: Optional[FilterArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_rsIDs(fields, rsIDs, QueryType.SNPS, page_args, filter_args)
    
    @strawberry.field
    async def get_aggs_by_RsIDs(self, info: Info, rsIDs: list[str],
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_rsIDs(fields, rsIDs, QueryType.AGGS, page_args, None, histogram)
    
    @strawberry.field
    async def count_SNPs_by_RsIDs(self, rsIDs: list[str], filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_rsIDs(rsIDs, filter_args)
    
    @strawberry.field
    async def download_SNPs_by_RsIDs(self, rsIDs: list[str], fields: list[str],
                             page_args: Optional[PageArgs] = None) -> str:
        return await search_by_rsIDs(fields, rsIDs, QueryType.DOWNLOAD, page_args)
    
     
    @strawberry.field
    async def get_SNPs_by_IDs(self, info: Info, ids: list[str],
                          page_args: Optional[PageArgs] = None,
                          filter_args: Optional[FilterArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_IDs(fields, ids, QueryType.SNPS, page_args, filter_args)
    
    @strawberry.field
    async def get_aggs_by_IDs(self, info: Info, ids: list[str],
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_IDs(fields, ids, QueryType.AGGS, page_args, None, histogram)
    
    @strawberry.field
    async def count_SNPs_by_IDs(self, ids: list[str], filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_IDs(ids, filter_args)
    
    @strawberry.field
    async def download_SNPs_by_IDs(self, ids: list[str], fields: list[str],
                          page_args: Optional[PageArgs] = None) -> str:
        return await search_by_IDs(fields, ids, QueryType.DOWNLOAD, page_args)
    
    
    @strawberry.field
    async def get_SNPs_by_gene_product(self, info: Info, gene: str,
                                   page_args: Optional[PageArgs] = None,
                                   filter_args: Optional[FilterArgs] = None) -> List[Snp]:
        fields = get_selected_fields(info)
        return await search_by_gene(fields, gene, QueryType.SNPS, page_args, filter_args)
    
    @strawberry.field
    async def get_aggs_by_gene_product(self, info: Info, gene: str,
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_gene(fields, gene, QueryType.AGGS, page_args, None, histogram)
    
    @strawberry.field
    async def count_SNPs_by_gene_product(self, gene: str, filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_gene(gene, filter_args)
    
    @strawberry.field
    async def download_SNPs_by_gene_product(self, gene: str, fields: list[str],
                                   page_args: Optional[PageArgs] = None) -> str:
        return await search_by_gene(fields, gene, QueryType.DOWNLOAD, page_args)