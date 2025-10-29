"""snp router."""

from fastapi import APIRouter, Depends, Query
from src.graphql.models.annotation_model import FilterArgs, PageArgs
from src.graphql.resolvers.api_snp_resolver import (
    search_by_chromosome,
    search_by_rsIDs,
    search_by_gene_product,
)
from src.graphql.resolvers.api_count_resolver import (
    count_by_chromosome,
    count_by_rsIDs,
    count_by_gene_product,
)
from src.graphql.models.return_info_model import OutputSnpInfo, OutputCountInfo
from src.data_adapter.snp_attributes import (
    get_snp_attrib_json,
)
from src.routers.snp_router_helpers import (
    MAX_ATTRIB_SIZE,
    MAX_PAGE_SIZE,
    ChromosomeIdentifierType,
    CommonSearchQueryParams,
    parse_filter_fields,
)
from src.routers.streaming import router as streaming_router

TITLE = "AnnoQ API"


SUMMARY = "API for accessing SNP data from Annoq.org"

DESCRIPTION = (
    "Programmatic access to SNP search, counting, and streaming downloads from Annoq.org. "
    "Use paginated endpoints for interactive exploration and the download routes for full-result exports."
)

VERSION = "2.5"

TAGS_METADATA = [
    {
        "name": "ATTRIBUTES",
        "description": (
            "Retrieve metadata for each available SNP attribute, including labels, friendly names, "
            "descriptions, data provenance, and keyword-search eligibility."
        ),
    },
    {
        "name": "SNP",
        "description": (
            "Retrieve SNPs by chromosome range, RSID list, or gene product. Each response always includes "
            f"the SNP identifier plus the attributes you request (maximum {MAX_ATTRIB_SIZE} per call)."
        ),
    },
    {
        "name": "Count",
        "description": (
            "Return the number of SNPs matching chromosome, RSID, or gene product filters with optional "
            "attribute-existence constraints."
        ),
    },
    {
        "name": "DOWNLOAD",
        "description": (
            "Download SNP annotations for large result sets exceeding pagination limits. Download by chromosome "
            "range or RSID list in CSV (default) or NDJSON format."
        ),
    },
]

router = APIRouter()
router.include_router(streaming_router)


@router.get(
    "/snpAttributes",
    tags=["ATTRIBUTES"],
    summary="List available SNP attributes",
    description=(
        "Returns metadata for every attribute that can be requested across the SNP endpoints, including "
        "labels, descriptions, source versions, and keyword-search support."
    ),
    response_description="Metadata describing each SNP attribute.",
)
async def get_snp_attributes():
    return get_snp_attrib_json()


@router.get(
    "/snp/chr",
    tags=["SNP"],
    summary="Search SNPs by chromosome range",
    description=(
        "Paginated search of SNPs within a chromosome interval.\n\n"
        "**Use when**\n"
        f"- Exploring result sets of up to {MAX_PAGE_SIZE} records.\n"
        "- Needing precise pagination controls (use `/download/chr` for bulk exports).\n\n"
        "**Key limits**\n"
        f"- `pagination_from + pagination_size` must be ≤ {MAX_PAGE_SIZE}.\n"
        f"- Request at most {MAX_ATTRIB_SIZE} attributes per call.\n"
        "- Positions are 1-based and inclusive."
    ),
    response_model=OutputSnpInfo,
    response_model_exclude_none=True,
    response_description="Paginated list of SNPs for the requested interval.",
)
async def get_snps_by_chr(
    chromosome_identifier: ChromosomeIdentifierType = Query(
        default=ChromosomeIdentifierType.CHR_1,
        description="Chromosome identifier (`1`–`22` or `X`).",
    ),
    start_position: int = Query(
        1, description="1-based inclusive start position for the search interval."
    ),
    end_position: int = Query(
        100000, description="1-based inclusive end position for the search interval."
    ),
    params: CommonSearchQueryParams = Depends(),
):
    page_args = PageArgs(from_=params.pagination_from, size=params.pagination_size)
    filter_args = (
        FilterArgs(exists=params._parsed_filter_fields)
        if params._parsed_filter_fields
        else None
    )

    attribs = params._parsed_fields

    return await search_by_chromosome(
        attribs,
        chromosome_identifier.value,
        start_position,
        end_position,
        page_args,
        filter_args,
    )


@router.get(
    "/snp/rsidList",
    tags=["SNP"],
    summary="Search SNPs by RSID list",
    description=(
        "Retrieves SNPs whose identifiers match the provided RSIDs.\n\n"
        "**Tips**\n"
        "- Supply RSIDs as a comma-separated list (whitespace is ignored).\n"
        "- Use pagination settings to browse results; switch to `/download/rsidList` for complete exports.\n"
        "**Key limits**\n"
        f"- `pagination_from + pagination_size` must be ≤ {MAX_PAGE_SIZE}.\n"
        f"- Attribute selection is limited to {MAX_ATTRIB_SIZE} fields per call."
    ),
    response_model=OutputSnpInfo,
    response_model_exclude_none=True,
    response_description="Paginated SNP results for the requested RSIDs.",
)
async def get_snps_by_rsidList(
    rsid_list: str = Query(
        default="rs1219648,rs2912774,rs2981582,rs1101006,rs1224211,rs1076148,rs2116830,rs1801516,rs2250417,rs1436109,rs1227926,rs1047964,rs900145,rs4757144,rs6486122,rs4627050,rs6578985,rs2074238,rs179429,rs231362,rs231906,rs108961,rs7481311",
        description="Comma-separated RSIDs (e.g. `rs574852966,rs148600903`).",
    ),
    params: CommonSearchQueryParams = Depends(),
):
    page_args = PageArgs(from_=params.pagination_from, size=params.pagination_size)
    filter_args = (
        FilterArgs(exists=params._parsed_filter_fields)
        if params._parsed_filter_fields
        else None
    )

    attribs = params._parsed_fields

    rsIDs = rsid_list.split(",")

    return await search_by_rsIDs(attribs, rsIDs, page_args, filter_args)


@router.get(
    "/snp/gene_product",
    tags=["SNP"],
    summary="Search SNPs by gene product",
    description=(
        "Returns SNPs linked to the supplied gene product (gene ID, symbol, or UniProt ID).\n\n"
        "**Use when** you need paginated SNP annotations tied to a single gene product. "
        f"Switch to `/download/gene_product` for large exports. Attribute requests remain capped at {MAX_ATTRIB_SIZE} fields.\n"
        "**Key limits**\n"
        f"- `pagination_from + pagination_size` must be ≤ {MAX_PAGE_SIZE}.\n"
    ),
    response_model=OutputSnpInfo,
    response_model_exclude_none=True,
    response_description="Paginated SNP results for the requested gene product.",
)
async def get_SNPs_by_gene_product(
    gene: str = Query(
        default="ZMYND11",
        description="Gene product identifier (gene ID, gene symbol, or UniProt ID).",
    ),
    params: CommonSearchQueryParams = Depends(),
):
    page_args = PageArgs(from_=params.pagination_from, size=params.pagination_size)
    filter_args = (
        FilterArgs(exists=params._parsed_filter_fields)
        if params._parsed_filter_fields
        else None
    )

    attribs = params._parsed_fields

    return await search_by_gene_product(attribs, gene, page_args, filter_args)


@router.get(
    "/fastapi/count/chr",
    tags=["Count"],
    summary="Count SNPs by chromosome range",
    description=(
        "Returns the number of SNP records within a chromosome interval. Apply `filter_fields` to require "
        "non-null values for specific attributes before counting."
    ),
    response_model=OutputCountInfo,
    response_description="Count of SNPs matching the chromosome interval and optional filters.",
)
async def count_snps_by_chromosome(
    chromosome_identifier: ChromosomeIdentifierType = Query(
        default=ChromosomeIdentifierType.CHR_1,
        description="Chromosome identifier (`1`–`22` or `X`).",
    ),
    start_position: int = Query(
        1, description="1-based inclusive start position for the count interval."
    ),
    end_position: int = Query(
        100000, description="1-based inclusive end position for the count interval."
    ),
    filter_fields: str = Query(
        default=None,
        description=(
            "Comma-separated attribute labels that must exist (non-null) for a record to be counted. "
            "Only valid attribute labels are applied."
        ),
    ),
):
    parsed_filter_fields = parse_filter_fields(filter_fields)
    if parsed_filter_fields is not None:
        filter_args = FilterArgs(exists=parsed_filter_fields)
    else:
        filter_args = None
    return await count_by_chromosome(
        chromosome_identifier.value, start_position, end_position, filter_args
    )


@router.get(
    "/fastapi/count/rsidList",
    tags=["Count"],
    summary="Count SNPs by RSID list",
    description=(
        "Returns how many SNPs in the system match the provided RSIDs, optionally enforcing attribute "
        "existence requirements via `filter_fields`."
    ),
    response_model=OutputCountInfo,
    response_description="Count of SNPs matching the RSID list and optional filters.",
)
async def count_snps_by_rsidList(
    rsid_list: str = Query(
        default="rs1219648,rs2912774,rs2981582,rs1101006,rs1224211,rs1076148,rs2116830,rs1801516,rs2250417,rs1436109,rs1227926,rs1047964,rs900145,rs4757144,rs6486122,rs4627050,rs6578985,rs2074238,rs179429,rs231362,rs231906,rs108961,rs7481311",
        description="Comma-separated RSIDs to count.",
    ),
    filter_fields: str = Query(
        default=None,
        description=(
            "Comma-separated attribute labels that must be present (non-null) in counted records. "
            "Unsupported labels are ignored."
        ),
    ),
):
    rsIDs = rsid_list.split(",")
    parsed_filter_fields = parse_filter_fields(filter_fields)
    if parsed_filter_fields is not None:
        filter_args = FilterArgs(exists=parsed_filter_fields)
    else:
        filter_args = None
    return await count_by_rsIDs(rsIDs, filter_args)


@router.get(
    "/fastapi/count/gene_product",
    tags=["Count"],
    summary="Count SNPs by gene product",
    description=(
        "Returns the number of SNPs associated with the specified gene product, with optional attribute "
        "existence filters."
    ),
    response_model=OutputCountInfo,
    response_description="Count of SNPs matching the gene product criteria.",
)
async def count_snps_by_gene_product(
    gene: str = Query(
        default="ZMYND11",
        description="Gene product identifier (gene ID, gene symbol, or UniProt ID).",
    ),
    filter_fields: str = Query(
        default=None,
        description=(
            "Comma-separated attribute labels that must be non-null for a record to be counted. "
            "Only valid labels are applied."
        ),
    ),
):
    parsed_filter_fields = parse_filter_fields(filter_fields)
    if parsed_filter_fields is not None:
        filter_args = FilterArgs(exists=parsed_filter_fields)
    else:
        filter_args = None
    return await count_by_gene_product(gene, filter_args)
