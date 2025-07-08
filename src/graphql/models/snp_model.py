from typing import List
import strawberry
from src.graphql.models.generated.snp import SnpModel
from src.graphql.models.generated.snp_aggs import SnpAggsModel
from typing import Optional

@strawberry.experimental.pydantic.type(model=SnpModel, all_fields=True)
class Snp:
    id: strawberry.ID = strawberry.field(description="This is a unique identifier for each record in the system.  It is a concatenation of the chromosome, followed by a colon (':'), followed by the position, followed by the reference nucleotide, followed by a greater than symbol ('<') followed by alternate nucleotide")
    pass

@strawberry.experimental.pydantic.type(model=SnpAggsModel, all_fields=True)
class SnpAggs:
    pass

@strawberry.type (
    description="This is a list of SNPs with associated attributes"
)
class SnpList:
    snps: List[Snp]


@strawberry.type
class ScrollSnp:
    snps: List[Snp]
    scroll_id: Optional[str] = None


@strawberry.type
class Gene:
    contig: str
    start: int
    end: int
    gene_id: str