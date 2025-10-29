from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
import orjson
from src.graphql.resolvers.api_snp_helper_resolver import convert_hits_to_output
from src.graphql.models.annotation_model import FilterArgs
from src.graphql.resolvers.large_result_streaming_resolver import (
    stream_by_chromosome,
    stream_by_gene_product,
    stream_by_rsIDs,
)
from src.routers.snp_router_helpers import (
    MAX_ATTRIB_SIZE,
    StreamingFormatType,
    StreamingQueryParams,
    ChromosomeIdentifierType,
)
from typing import AsyncIterator, List, Optional, Callable
import csv
from io import StringIO


router = APIRouter()

MAX_DOWNLOAD_SIZE = 1_000_000


def get_streaming_headers_and_media_type(format_type: str):
    """
    Returns appropriate headers and media type based on the format.
    """
    if format_type == "csv":
        headers = {
            "Content-Disposition": 'attachment; filename="export.csv"',
            "X-Accel-Buffering": "no",
        }
        media_type = "text/csv"
    else:  # ndjson
        headers = {
            "Content-Disposition": 'attachment; filename="export.ndjson"',
            "X-Accel-Buffering": "no",
        }
        media_type = "application/x-ndjson"

    return headers, media_type


async def generate_stream(
    stream_func: Callable,
    *args,
    format_type: StreamingFormatType,
    parsed_fields: List[str],
    **kwargs,
) -> AsyncIterator[bytes]:
    """
    Generic generator function that handles both CSV and NDJSON formats.
    """
    first_record = True

    async for snp in stream_func(*args, **kwargs):
        if format_type == StreamingFormatType.CSV:
            # For CSV format, create header and comma-separated values with proper escaping
            if first_record:
                # Create header row using csv.writer for proper escaping
                buffer = StringIO()
                writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(parsed_fields)
                yield buffer.getvalue().encode("utf-8")
                first_record = False

            # Create data row with proper CSV escaping
            buffer = StringIO()
            writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL)

            values = []
            for k in parsed_fields:
                if k == "id":
                    values.append(str(snp["_id"]))
                else:
                    # Get value, use empty string for missing fields instead of "."
                    value = snp["_source"].get(k, "")
                    # Convert to string, handle None values
                    values.append(str(value) if value is not None else "")

            writer.writerow(values)
            yield buffer.getvalue().encode("utf-8")
        else:  # ndjson format
            # jsonable_encoder -> orjson -> newline (NDJSON)
            output = convert_hits_to_output(parsed_fields, [snp])
            if hasattr(output, "details") and output.details:
                for snp in output.details:
                    yield orjson.dumps(jsonable_encoder(snp)) + b"\n"


async def create_streaming_response(
    stream_func: Callable,
    format_type: StreamingFormatType,
    parsed_fields: List[str],
    filter_args: Optional[FilterArgs],
    *args,
    **kwargs,
) -> StreamingResponse:
    """
    Creates a StreamingResponse with common logic for all download endpoints.
    """
    headers, media_type = get_streaming_headers_and_media_type(format_type)

    def generator():
        return generate_stream(
            stream_func,
            *args,
            format_type=format_type,
            parsed_fields=parsed_fields,
            filter_args=filter_args,
            **kwargs,
        )

    return StreamingResponse(generator(), media_type=media_type, headers=headers)


@router.post(
    "/snp/chr/download",
    tags=["DOWNLOAD"],
    summary="Download SNPs by chromosome range",
    description=(
        "Streams every SNP in the specified chromosome interval as CSV (default) or NDJSON without pagination.\n\n"
        "**Best for** large exports exceeding the 10,000-record pagination limit.\n"
        "**Constraints**\n"
        f"- Maximum of {MAX_ATTRIB_SIZE} requested attributes.\n"
        f"- Streaming stops after {MAX_DOWNLOAD_SIZE} records to protect the service."
    ),
)
async def download_snps_by_chr(
    chromosome_identifier: ChromosomeIdentifierType = Query(
        default=ChromosomeIdentifierType.CHR_1,
        description="Chromosome identifier (`1`–`22` or `X`).",
    ),
    start_position: int = Query(
        1, description="1-based inclusive start position for the download interval."
    ),
    end_position: int = Query(
        100000, description="1-based inclusive end position for the download interval."
    ),
    params: StreamingQueryParams = Depends(),
):
    filter_args = (
        FilterArgs(exists=params._parsed_filter_fields)
        if params._parsed_filter_fields
        else None
    )

    return await create_streaming_response(
        stream_by_chromosome,
        params.format,
        params._parsed_fields,
        filter_args,
        params._parsed_fields,
        chromosome_identifier.value,
        start_position,
        end_position,
        MAX_DOWNLOAD_SIZE,
    )


@router.post(
    "/snp/rsidList/download",
    tags=["DOWNLOAD"],
    summary="Download SNPs by RSID list",
    description=(
        "Streams all SNPs whose identifiers match the provided RSIDs as CSV (default) or NDJSON without pagination.\n"
        "Use this endpoint when you need the full result set in a single download."
    ),
)
async def download_snps_by_rsidList(
    rsid_list: str = Query(
        default="rs1219648,rs2912774,rs2981582,rs1101006,rs1224211,rs1076148,rs2116830,rs1801516,rs2250417,rs1436109,rs1227926,rs1047964,rs900145,rs4757144,rs6486122,rs4627050,rs6578985,rs2074238,rs179429,rs231362,rs231906,rs108961,rs7481311",
        description="Comma-separated RSIDs (e.g. `rs574852966,rs148600903`).",
    ),
    params: StreamingQueryParams = Depends(),
):
    filter_args = (
        FilterArgs(exists=params._parsed_filter_fields)
        if params._parsed_filter_fields
        else None
    )

    rsIDs = rsid_list.split(",")

    return await create_streaming_response(
        stream_by_rsIDs,
        params.format,
        params._parsed_fields,
        filter_args,
        params._parsed_fields,
        rsIDs,
        MAX_DOWNLOAD_SIZE,
    )


@router.post(
    "/snp/gene_product/download",
    tags=["DOWNLOAD"],
    summary="Download SNPs by gene product",
    description=(
        "Streams every SNP associated with the specified gene product (gene ID, symbol, or UniProt ID) "
        "as CSV (default) or NDJSON without pagination. Ideal for complete exports beyond the paginated search limit."
    ),
)
async def download_snps_by_gene_product(
    gene: str = Query(
        default="ZMYND11",
        description="Gene product identifier (gene ID, gene symbol, or UniProt ID).",
    ),
    params: StreamingQueryParams = Depends(),
):
    filter_args = (
        FilterArgs(exists=params._parsed_filter_fields)
        if params._parsed_filter_fields
        else None
    )

    return await create_streaming_response(
        stream_by_gene_product,
        params.format,
        params._parsed_fields,
        filter_args,
        params._parsed_fields,
        gene,
        MAX_DOWNLOAD_SIZE,
    )
