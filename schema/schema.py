from typing import List
import strawberry
from strawberry.types import Info
from models.model import AnnoqSampleData, PersonType, AnnoqDataType

from resolvers.resolver import get_annotations, get_sample_annotations, search_by_ID
from utils import get_selected_fields

@strawberry.type
class Query:

    @strawberry.field
    async def data_by_ID(self, info: Info, id: str) -> List[AnnoqSampleData]:
        return await search_by_ID(id)
    
    
    @strawberry.field
    async def sample_annotations(self, info: Info) -> List[AnnoqSampleData]:     
        return await get_sample_annotations()
    

    @strawberry.field
    async def annotations(self, info: Info) -> List[AnnoqDataType]: 
        fields = get_selected_fields(info)
        return await get_annotations(fields)
    
    @strawberry.field
    def hello(self) -> PersonType:
        person = PersonType(name='Alice', occupation='engineer')
        return person    


