import strawberry


@strawberry.type
class AnnoqData:
    id: strawberry.ID
    chr: str
    pos: int
    ref: str
    alt: str
    ANNOVAR_ensembl_Effect: str = None
    ANNOVAR_ensembl_Transcript_ID: str = None
    ANNOVAR_ensembl_Gene_ID: str = None
    ANNOVAR_ensembl_summary: str = None
    SnpEff_ensembl_Effect: str = None
    SnpEff_ensembl_Effect_impact: str = None
