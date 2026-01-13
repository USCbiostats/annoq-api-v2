python -m scripts.class_generators.generator

datamodel-codegen --input scripts/class_generators/generated_schemas/snp_schema.json --input-file-type jsonschema  --base-class src.graphql.models.model_config.ModelConfig  --output src/graphql/models/generated/snp.py
datamodel-codegen --input scripts/class_generators/generated_schemas/snp_aggs_schema.json --input-file-type jsonschema --base-class src.graphql.models.model_config.ModelConfig --output src/graphql/models/generated/snp_aggs.py

FILE="src/graphql/models/generated/snp_aggs.py"
SNP_FILE="src/graphql/models/generated/snp.py"
LINE="from typing import Any"
#REMOVE_TEXT="Any, "
sed -i "s/$LINE//g" $FILE

EXISTING_LINE="from pydantic import Field"
NEW_LINE="from src.graphql.models.annotation_model import AggregationItem"
sed -i "/$EXISTING_LINE/a $NEW_LINE" $FILE

FIND_TEXT="Any"
REPLACE_TEXT="AggregationItem"
sed -i "s/$FIND_TEXT/$REPLACE_TEXT/g" $FILE
sed -i 's/\\t//g' $FILE
sed -i 's/\\t//g' $SNP_FILE