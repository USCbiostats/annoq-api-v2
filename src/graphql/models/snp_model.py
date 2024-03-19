import strawberry
from scripts.class_generators.AnnoqData_class import AnnoqData


@strawberry.experimental.pydantic.type(model=AnnoqData, all_fields=True)
class AnnoqDataType:
    id: strawberry.ID
    pass