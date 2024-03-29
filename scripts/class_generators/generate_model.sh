python -m scripts.class_generators.generator

datamodel-codegen --input scripts/class_generators/class_schema.json --input-file-type jsonschema --output src/graphql/models/generated/snp.py

FILE="src/graphql/models/generated/snp.py"
LINE="from typing import Any, Optional"
REMOVE_TEXT="Any, "
sed -i "/$LINE/s/$REMOVE_TEXT//g" $FILE

EXISTING_LINE="from pydantic import BaseModel, Field"
NEW_LINE="from src.graphql.models.annotation_model import Annotation"
sed -i "/$EXISTING_LINE/a $NEW_LINE" $FILE

FIND_TEXT="Any"
REPLACE_TEXT="Annotation"
sed -i "s/$FIND_TEXT/$REPLACE_TEXT/g" $FILE