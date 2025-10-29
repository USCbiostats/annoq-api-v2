from pydantic import BaseModel, Field, model_validator
import json
from typing import List, Optional
from src.data_adapter.snp_attributes import get_attrib_list

# Constants
MAX_PAGE_SIZE = 10_000
MAX_ATTRIB_SIZE = 20


def parse_filter_fields(filter_fields: Optional[str]) -> List[str] | None:
    """
    Parse a comma-separated string of filter fields into a list.
    """
    if not filter_fields:
        return []
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
        default='{"_source":["Basic Info","chr","pos","ref","alt","rs_dbSNP151"]}',
        description="Contents of SNP configuration file generated from selected SNP attributes and downloaded from annoq.org.  The maximum number of attributes should not exceed "
        + str(MAX_ATTRIB_SIZE),
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
        description="SNP attribute labels (columns) that should not be empty for the record to be retrieved.  These are delimited by comma ','.  Example ANNOVAR_ucsc_Transcript_ID,VEP_ensembl_Gene_ID,SnpEff_ensembl_CDS_position_CDS_len,flanking_0_GO_biological_process_complete_list_id,flanking_0_GO_cellular_component_complete_list_id",
    )

    # The validated and cleaned list of fields will be stored here
    parsed_fields: List[str] = Field(default_factory=list, exclude=True)
    parsed_filter_fields: Optional[List[str]] = Field(default=None, exclude=True)

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
        self.parsed_fields = filtered_fields
        self.pagination_from = pagination_from

        # ---- Filter fields parsing ----
        self.parsed_filter_fields = parse_filter_fields(self.filter_fields)
        return self
