from typing import List
import strawberry
from src.graphql.models.generated.snp import SnpModel
from src.graphql.models.generated.snp_aggs import SnpAggsModel
from strawberry.experimental.pydantic import type as pydantic_type

@strawberry.experimental.pydantic.type(model=SnpModel, all_fields=True)
class Snp:
    id: strawberry.ID
    pass



@strawberry.experimental.pydantic.type(model=SnpAggsModel, all_fields=True)
class SnpAggs:
    pass

@strawberry.type
class SnpList:
    snps: List[Snp]