from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
import orjson
from pydantic import BaseModel, Field
from src.graphql.models.annotation_model import FilterArgs
from src.graphql.resolvers.large_result_streaming_resolver import (
    stream_by_chromosome,
    stream_by_gene_product,
    stream_by_rsIDs,
)
from src.routers.snp import ChromosomeIdentifierType
from src.routers.snp_router_helpers import (
    MAX_ATTRIB_SIZE,
    parse_filter_fields,
)
from src.data_adapter.snp_attributes import get_attrib_list
import json
from typing import AsyncIterator, List, Optional


class StreamingQueryParams(BaseModel):
    """
    Query params for streaming without pagination.
    """

    fields: str = Field(
        default='{"_source":["Basic Info","chr","pos","ref","alt","rs_dbSNP151"]}',
        description="Contents of SNP configuration file generated from selected SNP attributes and downloaded from annoq.org. The maximum number of attributes should not exceed "
        + str(MAX_ATTRIB_SIZE),
    )
    filter_fields: Optional[str] = Field(
        default=None,
        description="SNP attribute labels (columns) that should not be empty for the record to be retrieved. These are delimited by comma ','. Example ANNOVAR_ucsc_Transcript_ID,VEP_ensembl_Gene_ID,SnpEff_ensembl_CDS_position_CDS_len",
    )

    parsed_fields: List[str] = Field(default_factory=list, exclude=True)
    parsed_filter_fields: Optional[List[str]] = Field(default=None, exclude=True)

    def model_post_init(self, __context):
        """Parse and validate fields after initialization."""
        try:
            fields_json = json.loads(self.fields)
        except json.JSONDecodeError:
            raise ValueError("'fields' must be valid JSON.")

        if not isinstance(fields_json, dict) or "_source" not in fields_json:
            raise ValueError(
                "'fields' must contain a key '_source' with a list of field names."
            )

        source_fields = fields_json["_source"]
        if not isinstance(source_fields, list):
            raise ValueError("'_source' must be a list of field names.")

        allowed_fields = get_attrib_list() or []
        filtered_fields = [f for f in source_fields if f in allowed_fields]

        if not filtered_fields:
            raise ValueError("Please provide at least one valid field.")

        if len(filtered_fields) > MAX_ATTRIB_SIZE:
            raise ValueError(
                f"Number of requested attributes ({len(filtered_fields)}) exceeds maximum allowed ({MAX_ATTRIB_SIZE})."
            )

        self.parsed_fields = filtered_fields
        self.parsed_filter_fields = parse_filter_fields(self.filter_fields)


router = APIRouter()

MAX_DOWNLOAD_SIZE = 1_000_000_000


@router.post(
    "/download/chr",
    tags=["DOWNLOAD"],
    description="Stream all SNPs by chromosome id and position range in NDJson format. Returns complete result set without pagination.",
)
async def download_snps_by_chr(
    chromosome_identifier: ChromosomeIdentifierType = Query(
        default=ChromosomeIdentifierType.CHR_1, description="Chromosome id to search."
    ),
    start_position: int = Query(1, description="Start position region of search"),
    end_position: int = Query(100000, description="End position region of search"),
    params: StreamingQueryParams = Depends(),
):
    filter_args = (
        FilterArgs(exists=params.parsed_filter_fields)
        if params.parsed_filter_fields
        else None
    )

    headers = {
        "Content-Disposition": 'attachment; filename="export.ndjson"',
        "X-Accel-Buffering": "no",
    }

    async def generate() -> AsyncIterator[bytes]:
        async for snp in stream_by_chromosome(
            params.parsed_fields,
            chromosome_identifier.value,
            start_position,
            end_position,
            MAX_DOWNLOAD_SIZE,
            filter_args,
        ):
            # jsonable_encoder -> orjson -> newline (NDJSON)
            payload = jsonable_encoder(snp)
            yield orjson.dumps(payload) + b"\n"

    return StreamingResponse(
        generate(), media_type="application/x-ndjson", headers=headers
    )


@router.post(
    "/download/rsidList",
    tags=["DOWNLOAD"],
    description="Stream SNPs for specified list of RSIDs in NDJson format. Returns complete result set without pagination.",
)
async def download_snps_by_rsidList(
    rsid_list: str = Query(
        default="rs1219648,rs2912774,rs2981582,rs1101006,rs1224211,rs1076148,rs2116830,rs1801516,rs2250417,rs1436109,rs1227926,rs1047964,rs900145,rs4757144,rs6486122,rs4627050,rs6578985,rs2074238,rs179429,rs231362,rs231906,rs108961,rs7481311",
        description="List of RSIDS to search. Delimited by comma ','. Example rs574852966,rs148600903",
    ),
    params: StreamingQueryParams = Depends(),
):
    filter_args = (
        FilterArgs(exists=params.parsed_filter_fields)
        if params.parsed_filter_fields
        else None
    )

    rsIDs = rsid_list.split(",")

    headers = {
        "Content-Disposition": 'attachment; filename="export.ndjson"',
        "X-Accel-Buffering": "no",
    }

    async def generate() -> AsyncIterator[bytes]:
        async for snp in stream_by_rsIDs(
            params.parsed_fields,
            rsIDs,
            MAX_DOWNLOAD_SIZE,
            filter_args,
        ):
            # jsonable_encoder -> orjson -> newline (NDJSON)
            payload = jsonable_encoder(snp)
            yield orjson.dumps(payload) + b"\n"

    return StreamingResponse(
        generate(), media_type="application/x-ndjson", headers=headers
    )


@router.post(
    "/download/gene_product",
    tags=["DOWNLOAD"],
    description="Stream SNPs for specified gene product (gene id, gene symbol or UniProt id) in NDJson format. Returns complete result set without pagination.",
)
async def download_snps_by_gene_product(
    gene: str = Query(default="ZMYND11", description="Gene product search"),
    params: StreamingQueryParams = Depends(),
):
    filter_args = (
        FilterArgs(exists=params.parsed_filter_fields)
        if params.parsed_filter_fields
        else None
    )

    headers = {
        "Content-Disposition": 'attachment; filename="export.ndjson"',
        "X-Accel-Buffering": "no",
    }

    async def generate() -> AsyncIterator[bytes]:
        async for snp in stream_by_gene_product(
            params.parsed_fields,
            gene,
            MAX_DOWNLOAD_SIZE,
            filter_args,
        ):
            # jsonable_encoder -> orjson -> newline (NDJSON)
            payload = jsonable_encoder(snp)
            yield orjson.dumps(payload) + b"\n"

    return StreamingResponse(
        generate(), media_type="application/x-ndjson", headers=headers
    )
