from typing import List
import strawberry
from strawberry.types import Info
from models.model import AnnoqSampleData, PersonType, AnnoqDataType

from resolvers.resolver import get_annotations, search_by_ID

@strawberry.type
class Query:

    @strawberry.field
    async def get_data_by_ID(self, info: Info, id: str) -> List[AnnoqSampleData]:
        return await search_by_ID(id)
    

    @strawberry.field
    async def get_annotations(self, info: Info) -> List[AnnoqDataType]:
        return await get_annotations()
    
    @strawberry.field
    def hello(self) -> PersonType:
        person = PersonType(name='Alice', occupation='engineer')
        return person    


