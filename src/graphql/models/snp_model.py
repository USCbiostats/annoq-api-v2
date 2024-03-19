import strawberry
from scripts.class_generators.Snps import Snps


@strawberry.experimental.pydantic.type(model=Snps, all_fields=True)
class SnpsType:
    id: strawberry.ID
    pass