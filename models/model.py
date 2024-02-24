import strawberry
from typing import Optional

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
