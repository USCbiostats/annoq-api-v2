import strawberry
from typing import Optional
from models.generated_class import Person
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


@strawberry.experimental.pydantic.type(model=Person, all_fields=True)
class PersonType:
    pass


@strawberry.experimental.pydantic.type(model=AnnoqData, all_fields=True)
class AnnoqDataType:
    pass
