import strawberry
from src.graphql.models.generated.snp import Snp


@strawberry.experimental.pydantic.type(model=Snp, all_fields=True)
class SnpsType:
    id: strawberry.ID
    pass