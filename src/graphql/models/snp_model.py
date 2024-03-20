import strawberry
from .Snps import Snps


@strawberry.experimental.pydantic.type(model=Snps, all_fields=True)
class SnpsType:
    id: strawberry.ID
    pass