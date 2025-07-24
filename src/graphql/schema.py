from typing import List, Optional
import strawberry
from strawberry.types import Info
from src.graphql.gene_pos import get_pos_from_gene_id, map_gene, chromosomal_location_dic
from src.graphql.models.snp_model import Gene, ScrollSnp, SnpAggs
from src.graphql.models.annotation_model import FilterArgs, Histogram, PageArgs, QueryType, QueryTypeOption

from src.graphql.resolvers.snp_resolver import get_annotations, scroll_annotations_, search_by_chromosome, search_by_gene, search_by_keyword, search_by_rsID, search_by_rsIDs, search_by_IDs
from src.graphql.resolvers.count_resolver import count_by_IDs, count_by_chromosome, count_by_gene, count_by_keyword, count_by_rsID, count_by_rsIDs, get_annotations_count
from src.utils import get_selected_fields, get_sub_selected_fields, get_aggregation_fields
from src.data_adapter.snp_attributes import get_cleaned_to_actual_label_lookup


def transform_fields(fields:list[str]):
    lookup = get_cleaned_to_actual_label_lookup()
    transformed = []
    for field in fields:
        if field in lookup:
            transformed.append(lookup[field])
        else:
            print(f" field {field} not transformed")    
    return transformed


def transform_agg_fields(aggregation_fields: list[tuple[str, list[str]]]):
    transformed = []
    lookup = get_cleaned_to_actual_label_lookup()
    for field, subfields in aggregation_fields:
        if field in lookup:
            transformed.append((lookup[field], subfields))
        else:
            print(f" aggregate field {field} not transformed")               
    return transformed

def transform_filter_args(filter: FilterArgs=None):
    if filter is None:
        return None
    if filter.exists is None:
        return filter
    
    transformed_args = transform_fields(filter.exists)
    return FilterArgs(exists=transformed_args)
    
          


class CustomError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
@strawberry.type
class Query:
    
    @strawberry.field
    async def annotations(self, info: Info) -> ScrollSnp:
        try:
            fields = get_selected_fields(info)
            return await get_annotations(transform_fields(fields), QueryType.SNPS)
        except Exception as e:
            raise CustomError(str(e))
    
    @strawberry.field
    async def count_annotations(self) -> int: 
        return await get_annotations_count()
    
    @strawberry.field
    async def download_annotations(self, fields: list[str]) -> str: 
        return await get_annotations(transform_fields(fields), QueryType.DOWNLOAD)
    
    @strawberry.field
    async def scroll_annotations(self, info: Info, scroll_id: Optional[str] = None) -> ScrollSnp: 
        fields = get_sub_selected_fields(info)
        return await scroll_annotations_(transform_fields(fields), scroll_id)
    

    @strawberry.field
    async def get_SNPs_by_chromosome(self, info: Info, chr: str, start: int, end: int, query_type_option: QueryTypeOption,
                                  page_args: Optional[PageArgs] = None,
                                  filter_args: Optional[FilterArgs] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        if query_type_option == QueryTypeOption.SNPS:
            query_type = QueryType.SNPS
        else:
            query_type = QueryType.SCROLL
        return await search_by_chromosome(transform_fields(fields), chr, start, end, query_type, None, page_args, transform_filter_args(filter_args))
    
    @strawberry.field
    async def get_aggs_by_chromosome(self, info: Info, chr: str, start: int, end: int,
                                  page_args: Optional[PageArgs] = None, histogram: Optional[Histogram] = None, filter_args: Optional[FilterArgs] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        aggregation_fields = get_aggregation_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_chromosome(transform_fields(fields), chr, start, end, QueryType.AGGS, transform_agg_fields(aggregation_fields), page_args, transform_filter_args(filter_args), histogram)
    
    @strawberry.field
    async def count_SNPs_by_chromosome(self, chr: str, start: int, end: int, filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_chromosome(chr, start, end, transform_filter_args(filter_args))
    
    @strawberry.field
    async def download_SNPs_by_chromosome(self, chr: str, start: int, end: int, fields: list[str],
                                  page_args: Optional[PageArgs] = None, filter_args: Optional[FilterArgs] = None) -> str:
        return await search_by_chromosome(transform_fields(fields), chr, start, end, QueryType.DOWNLOAD, None, page_args, transform_filter_args(filter_args)) 
    

    @strawberry.field
    async def get_SNPs_by_RsID(self, info: Info, rsID: str, query_type_option: QueryTypeOption,
                            page_args: Optional[PageArgs] = None,
                            filter_args: Optional[FilterArgs] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        if query_type_option == QueryTypeOption.SNPS:
            query_type = QueryType.SNPS
        else:
            query_type = QueryType.SCROLL
        return await search_by_rsID(transform_fields(fields), rsID, query_type, None, page_args, transform_filter_args(filter_args))
    
    @strawberry.field
    async def get_aggs_by_RsID(self, info: Info, rsID: str,
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None, filter_args: Optional[FilterArgs] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        aggregation_fields = get_aggregation_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_rsID(transform_fields(fields), rsID, QueryType.AGGS, transform_agg_fields(aggregation_fields), page_args, transform_filter_args(filter_args), histogram)
    
    @strawberry.field
    async def count_SNPs_by_RsID(self, rsID: str, filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_rsID(rsID, transform_filter_args(filter_args))
    
    @strawberry.field
    async def download_SNPs_by_RsID(self, rsID: str, fields: list[str],
                            page_args: Optional[PageArgs] = None, filter_args: Optional[FilterArgs] = None) -> str:
        return await search_by_rsID(transform_fields(fields), rsID, QueryType.DOWNLOAD, None, page_args, transform_filter_args(filter_args))
    

    @strawberry.field
    async def get_SNPs_by_RsIDs(self, info: Info, rsIDs: list[str], query_type_option: QueryTypeOption,
                             page_args: Optional[PageArgs] = None,
                             filter_args: Optional[FilterArgs] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        if query_type_option == QueryTypeOption.SNPS:
            query_type = QueryType.SNPS
        else:
            query_type = QueryType.SCROLL
        return await search_by_rsIDs(transform_fields(fields), rsIDs, query_type, None, page_args, transform_filter_args(filter_args))
    
    @strawberry.field
    async def get_aggs_by_RsIDs(self, info: Info, rsIDs: list[str],
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None, filter_args: Optional[FilterArgs] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        aggregation_fields = get_aggregation_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_rsIDs(transform_fields(fields), rsIDs, QueryType.AGGS, transform_agg_fields(aggregation_fields), page_args, transform_filter_args(filter_args), histogram)
    
    @strawberry.field
    async def count_SNPs_by_RsIDs(self, rsIDs: list[str], filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_rsIDs(rsIDs, transform_filter_args(filter_args))
    
    @strawberry.field
    async def download_SNPs_by_RsIDs(self, rsIDs: list[str], fields: list[str],
                             page_args: Optional[PageArgs] = None, filter_args: Optional[FilterArgs] = None) -> str:
        return await search_by_rsIDs(transform_fields(fields), rsIDs, QueryType.DOWNLOAD, None, page_args, transform_filter_args(filter_args))
    
     
    @strawberry.field
    async def get_SNPs_by_IDs(self, info: Info, ids: list[str], query_type_option: QueryTypeOption,
                          page_args: Optional[PageArgs] = None,
                          filter_args: Optional[FilterArgs] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        if query_type_option == QueryTypeOption.SNPS:
            query_type = QueryType.SNPS
        else:
            query_type = QueryType.SCROLL
        return await search_by_IDs(transform_fields(fields), ids, query_type, None, page_args, transform_filter_args(filter_args))
    
    @strawberry.field
    async def get_aggs_by_IDs(self, info: Info, ids: list[str],
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None, filter_args: Optional[FilterArgs] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        aggregation_fields = get_aggregation_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_IDs(transform_fields(fields), ids, QueryType.AGGS, transform_agg_fields(aggregation_fields), page_args, transform_filter_args(filter_args), histogram)
    
    @strawberry.field
    async def count_SNPs_by_IDs(self, ids: list[str], filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_IDs(ids, transform_filter_args(filter_args))
    
    @strawberry.field
    async def download_SNPs_by_IDs(self, ids: list[str], fields: list[str],
                          page_args: Optional[PageArgs] = None, filter_args: Optional[FilterArgs] = None) -> str:
        return await search_by_IDs(transform_fields(fields), ids, QueryType.DOWNLOAD, None, page_args, transform_filter_args(filter_args))
    
    
    @strawberry.field
    async def get_SNPs_by_gene_product(self, info: Info, gene: str, query_type_option: QueryTypeOption,
                                   page_args: Optional[PageArgs] = None,
                                   filter_args: Optional[FilterArgs] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        if query_type_option == QueryTypeOption.SNPS:
            query_type = QueryType.SNPS
        else:
            query_type = QueryType.SCROLL
        return await search_by_gene(transform_fields(fields), gene, query_type, None, page_args, transform_filter_args(filter_args))
    
    @strawberry.field
    async def get_aggs_by_gene_product(self, info: Info, gene: str, 
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None, filter_args: Optional[FilterArgs] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        aggregation_fields = get_aggregation_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_gene(transform_fields(fields), gene, QueryType.AGGS, transform_agg_fields(aggregation_fields), page_args, transform_filter_args(filter_args), histogram)
    
    @strawberry.field
    async def count_SNPs_by_gene_product(self, gene: str, filter_args: Optional[FilterArgs] = None) -> int:
        return await count_by_gene(gene, transform_filter_args(filter_args))
    
    @strawberry.field
    async def download_SNPs_by_gene_product(self, gene: str, fields: list[str],
                                   page_args: Optional[PageArgs] = None, filter_args: Optional[FilterArgs] = None) -> str:
        return await search_by_gene(transform_fields(fields), gene, QueryType.DOWNLOAD, None, page_args, transform_filter_args(filter_args))
    
    @strawberry.field
    async def gene_info(self, gene: str) -> Gene:
        gene_id = map_gene(gene)
        gene_pos = get_pos_from_gene_id(gene_id, chromosomal_location_dic)
        if gene_pos:
            return Gene(contig=gene_pos[0], start=gene_pos[1], end=gene_pos[2], gene_id=gene_id)
        else:
            raise KeyError(f'Gene {gene} not found')
                                    
    @strawberry.field
    async def get_SNPs_by_keyword(self, info: Info, keyword: str, query_type_option: QueryTypeOption,
                            page_args: Optional[PageArgs] = None) -> ScrollSnp:
        fields = get_sub_selected_fields(info)
        if query_type_option == QueryTypeOption.SNPS:
            query_type = QueryType.SNPS
        else:
            query_type = QueryType.SCROLL
        return await search_by_keyword(transform_fields(fields), keyword, query_type, None, page_args)
    
    @strawberry.field
    async def get_aggs_by_keyword(self, info: Info, keyword: str,
                                  page_args: Optional[PageArgs] = None,
                                  histogram: Optional[Histogram] = None) -> SnpAggs:
        fields = get_selected_fields(info)
        aggregation_fields = get_aggregation_fields(info)
        if page_args is not None:
            page_args.size = 0
        return await search_by_keyword(transform_fields(fields), keyword, QueryType.AGGS, transform_agg_fields(aggregation_fields), page_args, histogram)
    
    @strawberry.field
    async def count_SNPs_by_keyword(self, keyword: str) -> int:
        return await count_by_keyword(keyword)
    
    @strawberry.field
    async def download_SNPs_by_keyword(self, keyword: str, fields: list[str],
                            page_args: Optional[PageArgs] = None) -> str:
        return await search_by_keyword(transform_fields(fields), keyword, QueryType.DOWNLOAD, None, page_args)
