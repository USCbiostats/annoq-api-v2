import strawberry
from typing import Optional
from models.AnnoqData_class import AnnoqData

@strawberry.type
class AnnoqSampleData:
    id: strawberry.ID
    chr: str
    pos: int
    ref: str
    alt: str
    ANNOVAR_ensembl_Effect: str
    ANNOVAR_ensembl_Transcript_ID: Optional[str]
    ANNOVAR_ensembl_Gene_ID: Optional[str]
    ANNOVAR_ensembl_summary: str
    SnpEff_ensembl_Effect: str
    SnpEff_ensembl_Effect_impact: str


@strawberry.experimental.pydantic.type(model=AnnoqData, all_fields=True)
class AnnoqDataType:
    pass

@strawberry.input
class PageArgs:
    _from: Optional[int] = 0
    size: Optional[int] = 50
