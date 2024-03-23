import strawberry
from src.graphql.models.generated.snp import Snps


@strawberry.experimental.pydantic.type(model=Snps, all_fields=True)
class SnpsType:
    id: strawberry.ID
    pass