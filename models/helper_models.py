import strawberry
from typing import Optional

@strawberry.input
class PageArgs:
    from_: Optional[int] = 0
    size: Optional[int] = 50


@strawberry.type
class AggregationItem:    
    doc_count: int

@strawberry.type
class Field:
    value: str
    aggs: Optional[AggregationItem] = None