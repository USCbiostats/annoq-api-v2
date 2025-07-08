from typing import List
from pydantic import BaseModel
#import strawberry
#from src.graphql.models.snp_model import SnpList, Snp
from src.graphql.models.generated.snp import SnpModel
#from src.graphql.models.annotation_model import DocCount



class OperationInfo(BaseModel):
    success: bool
    message: str

class OutputSnpInfo(OperationInfo):
    details: List[SnpModel]
    
class OutputCountInfo(OperationInfo):
    details: int    
    
    
    