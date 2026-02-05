from pydantic import BaseModel, Field, model_validator, PrivateAttr
import json
from typing import List, Optional
from src.data_adapter.snp_attributes import get_attrib_list
from src.config.settings import settings
from enum import Enum

# Constants
MAX_PAGE_SIZE = 10_000
MAX_ATTRIB_SIZE = 20

DEFAULT_SEARCH_PARAM = '{"_source":["Basic Info","chr","pos","ref","alt","' + settings.DATA_RSID + '"]}'

CHR_1 = "1"
CHR_2 = "2"
CHR_3 = "3"
CHR_4 = "4"
CHR_5 = "5"
CHR_6 = "6"
CHR_7 = "7"
CHR_8 = "8"
CHR_9 = "9"
CHR_10 = "10"
CHR_11 = "11"
CHR_12 = "12"
CHR_13 = "13"
CHR_14 = "14"
CHR_15 = "15"
CHR_16 = "16"
CHR_17 = "17"
CHR_18 = "18"
CHR_19 = "19"
CHR_20 = "20"
CHR_21 = "21"
CHR_22 = "22"
CHR_X = "X"


class ChromosomeIdentifierType(str, Enum):
    CHR_1 = CHR_1
    CHR_2 = CHR_2
    CHR_3 = CHR_3
    CHR_4 = CHR_4
    CHR_5 = CHR_5
    CHR_6 = CHR_6
    CHR_7 = CHR_7
    CHR_8 = CHR_8
    CHR_9 = CHR_9
    CHR_10 = CHR_10
    CHR_11 = CHR_11
    CHR_12 = CHR_12
    CHR_13 = CHR_13
    CHR_14 = CHR_14
    CHR_15 = CHR_15
    CHR_16 = CHR_16
    CHR_17 = CHR_17
    CHR_18 = CHR_18
    CHR_19 = CHR_19
    CHR_20 = CHR_20
    CHR_21 = CHR_21
    CHR_22 = CHR_22
    CHR_X = CHR_X


def parse_filter_fields(filter_fields: Optional[str]) -> List[str] | None:
    """
    Parse a comma-separated string of filter fields into a list of valid attribute labels.
    Returns None when no filters are supplied or no valid labels remain after validation.
    """
    if not filter_fields:
        return None
    allowed_fields = get_attrib_list() or []
    filtered_list = [
        f.strip() for f in filter_fields.split(",") if f.strip() in allowed_fields
    ]
    return filtered_list or None


class CommonSearchQueryParams(BaseModel):
    """
    Common reusable query params for pagination and field selection.
    Performs validation and cleanup of input.
    """

    fields: str = Field(
        #default='{"_source":["Basic Info","chr","pos","ref","alt","rs_dbSNP151"]}',
        detault=DEFAULT_SEARCH_PARAM,
        description=(
            "Contents of SNP configuration file generated from selected SNP attributes and downloaded from annoq.org. "
            "JSON object containing a `_source` array with the requested attribute labels. "
            f"Request at most {MAX_ATTRIB_SIZE} attributes per call; unknown labels are ignored."
        ),
    )
    pagination_from: Optional[int] = Field(
        default=0, description="starting index for pagination (0-based)."
    )
    pagination_size: int = Field(
        default=50,
        description="Number of results per page.  Maximum is " + str(MAX_PAGE_SIZE),
        le=MAX_PAGE_SIZE,
    )
    filter_fields: Optional[str] = Field(
        default=None,
        description=(
            "Comma-separated attribute labels that must contain data in the response (e.g. "
            "`ANNOVAR_ucsc_Transcript_ID,VEP_ensembl_Gene_ID`). Invalid labels are ignored."
        ),
    )

    # The validated and cleaned list of fields will be stored here
    _parsed_fields: List[str] = PrivateAttr(default_factory=list)
    _parsed_filter_fields: Optional[List[str]] = PrivateAttr(default=None)

    @model_validator(mode="after")
    def validate_logic(self):
        """
        Complex cross-field validation:
        - Validate pagination
        - Parse and clean 'fields' JSON
        - Filter fields by allowed set
        """
        # ---- Pagination validation ----
        pagination_from = self.pagination_from or 0
        if self.pagination_size <= 0:
            raise ValueError("pagination_size must be greater than 0")

        if pagination_from + self.pagination_size > MAX_PAGE_SIZE:
            raise ValueError(
                f"Requested range exceeds MAX_PAGE_SIZE ({MAX_PAGE_SIZE}). "
                f"pagination_from + pagination_size must be <= {MAX_PAGE_SIZE}."
            )

        # ---- Fields validation ----
        try:
            fields_json = json.loads(self.fields)
        except json.JSONDecodeError:
            raise ValueError("'fields' must be valid JSON.")
        except Exception as e:
            raise ValueError(f"Error parsing 'fields': {str(e)}")

        if not isinstance(fields_json, dict) or "_source" not in fields_json:
            raise ValueError(
                "'fields' must contain a key '_source' with a list of field names."
            )

        source_fields = fields_json["_source"]
        if not isinstance(source_fields, list):
            raise ValueError("'_source' must be a list of field names.")

        # ---- Filter against allowed attribute list ----
        allowed_fields = get_attrib_list() or []
        filtered_fields = [f for f in source_fields if f in allowed_fields]

        # Warn (silently ignore) if fields were removed
        if not filtered_fields:
            raise ValueError("Please provide at least one valid field.")

        if len(filtered_fields) > MAX_ATTRIB_SIZE:
            raise ValueError(
                f"Number of requested attributes ({len(filtered_fields)}) exceeds maximum allowed ({MAX_ATTRIB_SIZE})."
            )

        # Replace the string with structured data
        self._parsed_fields = filtered_fields
        self.pagination_from = pagination_from

        # ---- Filter fields parsing ----
        self._parsed_filter_fields = parse_filter_fields(self.filter_fields)
        return self


class StreamingFormatType(str, Enum):
    CSV = "csv"
    NDJSON = "ndjson"


class StreamingQueryParams(BaseModel):
    """
    Query params for download endpoints (no pagination, full-result streaming).
    """

    fields: str = Field(
        #default='{"_source":["Basic Info","chr","pos","ref","alt","rs_dbSNP151"]}',
        default=DEFAULT_SEARCH_PARAM,
        description=(
            "JSON payload with a `_source` list of attribute labels selected from the configuration "
            f"downloaded at annoq.org. Request at most {MAX_ATTRIB_SIZE} attributes per download call."
        ),
    )
    filter_fields: Optional[str] = Field(
        default=None,
        description=(
            "Comma-separated attribute labels that must be non-null in streamed records. "
            "Only valid labels are applied; others are ignored."
        ),
    )
    format: StreamingFormatType = Field(
        default=StreamingFormatType.CSV,
        description="Output format: 'csv' (default) or 'ndjson'",
    )

    _parsed_fields: List[str] = PrivateAttr(default_factory=list)
    _parsed_filter_fields: Optional[List[str]] = PrivateAttr(default=None)

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

        self._parsed_fields = filtered_fields
        self._parsed_filter_fields = parse_filter_fields(self.filter_fields)
