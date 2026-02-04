import re
import json
from strawberry.types import Info


class FieldNameMapper:
    """
    Centralized field name transformation handler.
    Maintains bidirectional mapping between original ES field names and cleaned API field names.
    Single source of truth for all field name transformations.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._cleaned_to_original: dict[str, str] = {}
        self._original_to_cleaned: dict[str, str] = {}
        self._initialized = True

    @staticmethod
    def _clean_name(name: str) -> str:
        """
        Transform an original field name to a cleaned API-compatible name.
        Rules:
        - Prefix with _ if starts with digit
        - Remove parentheses and their content
        - Replace / with _
        - Replace - with _
        - Remove + character
        """
        if name[0].isdigit():
            cleaned = f"_{name}"
        else:
            cleaned = name
        cleaned = re.sub(r"\([^)]*\)", "", cleaned)
        cleaned = cleaned.replace("/", "_")
        cleaned = cleaned.replace("-", "_")
        cleaned = cleaned.replace("+", "")
        cleaned = cleaned.replace('=', '_equals_')
        return cleaned

    def register_field(self, original_name: str) -> str:
        """
        Register an original field name and return its cleaned version.
        Stores the bidirectional mapping for later retrieval.
        """
        cleaned = self._clean_name(original_name)
        self._cleaned_to_original[cleaned] = original_name
        self._original_to_cleaned[original_name] = cleaned
        return cleaned

    def clean_field_name(self, name: str) -> str:
        """
        Get the cleaned field name. If not already registered, register it first.
        """
        if name in self._original_to_cleaned:
            return self._original_to_cleaned[name]
        return self.register_field(name)

    def get_original_name(self, cleaned_name: str) -> str | None:
        """
        Get the original ES field name from a cleaned API field name.
        Returns None if the cleaned name is not found in the mapping.
        """
        return self._cleaned_to_original.get(cleaned_name)

    def get_original_name_or_self(self, cleaned_name: str) -> str:
        """
        Get the original ES field name from a cleaned API field name.
        Returns the cleaned name itself if not found (for fields that don't need transformation).
        """
        return self._cleaned_to_original.get(cleaned_name, cleaned_name)

    def get_cleaned_to_original_lookup(self) -> dict[str, str]:
        """
        Returns the full mapping from cleaned names to original names.
        """
        return self._cleaned_to_original.copy()

    def get_original_to_cleaned_lookup(self) -> dict[str, str]:
        """
        Returns the full mapping from original names to cleaned names.
        """
        return self._original_to_cleaned.copy()

    def initialize_from_anno_tree(self, anno_tree_path: str = "./data/anno_tree.json"):
        """
        Initialize the mappings from the anno_tree.json file.
        This should be called at application startup.
        """
        with open(anno_tree_path) as f:
            data = json.load(f)
            for elt in data:
                if elt.get("leaf", False):
                    self.register_field(elt["name"])


# Global singleton instance
field_name_mapper = FieldNameMapper()


def clean_field_name(name: str) -> str:
    """
    Transform an original field name to a cleaned API-compatible name.
    This is the primary function to use for forward transformation.
    """
    return field_name_mapper.clean_field_name(name)


def get_original_field_name(cleaned_name: str) -> str | None:
    """
    Get the original ES field name from a cleaned API field name.
    Returns None if not found.
    """
    return field_name_mapper.get_original_name(cleaned_name)


def get_original_field_name_or_self(cleaned_name: str) -> str:
    """
    Get the original ES field name from a cleaned API field name.
    Returns the cleaned name itself if not found.
    """
    return field_name_mapper.get_original_name_or_self(cleaned_name)


def get_cleaned_to_original_lookup() -> dict[str, str]:
    """
    Returns the full mapping from cleaned names to original names.
    """
    return field_name_mapper.get_cleaned_to_original_lookup()


def get_selected_fields(info: Info):
    selected_fields = [field.name for field in info.selected_fields[0].selections]
    return selected_fields


def get_sub_selected_fields(info: Info):
    selected_fields = []
    for selection in info.selected_fields[0].selections:
        if selection.name == "snps":
            for sub_selection in selection.selections:
                selected_fields.append(sub_selection.name)
    return selected_fields


def get_aggregation_fields(info: Info) -> list[tuple[str, list[str]]]:
    """
    Get aggregation fields from the query, along with the subfields
    """

    aggregation_fields = []
    for field in info.selected_fields[0].selections:
        aggregation_fields.append(
            (field.name, [subfield.name for subfield in field.selections])
        )
    return aggregation_fields
