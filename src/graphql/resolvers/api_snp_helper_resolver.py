from src.graphql.models.return_info_model import OutputSnpInfo
from src.graphql.models.generated.snp import SnpModel
from src.utils import clean_field_name
from src.data_adapter.snp_attributes import get_version_info


def output_error_msg(message: str):
    return OutputSnpInfo(success=False, message=message)


def convert_hits_to_output(es_fields: list[str], hits: list):
    """
    Converts hits from elasticsearch to OutputSnpInfo object

    Params: es_fields: List of fields requested
            hits: hits from elasticsearch

    Returns: OutputSnpInfo object
    """
    compliant_results = []
    for hit in hits:
        source = hit["_source"]
        values = {clean_field_name(key): value for key, value in source.items()}
        compliant_results.append(SnpModel(**values))

    return OutputSnpInfo(
        success=True,
        message="OK",
        details=compliant_results,
        version=get_version_info(es_fields),
    )
