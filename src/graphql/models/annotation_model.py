from enum import Enum
import strawberry
from typing import Optional

@strawberry.input
class PageArgs:
    from_: Optional[int] = 0
    size: Optional[int] = 50

@strawberry.type
class Bucket:
    key: str
    doc_count: int

@strawberry.type
class DocCount:
    doc_count: int

@strawberry.type
class AggregationItem:    
    doc_count: int
    min: Optional[float] = None
    max: Optional[float] = None
    histogram: Optional[list[Bucket]] = None
    frequency: Optional[list[Bucket]] = None
    missing: Optional[DocCount] = None

@strawberry.type
class Annotation:
    value: str
    aggs: Optional[AggregationItem] = None

class QueryType(Enum):
    DOWNLOAD = 'DOWNLOAD'
    SNPS = 'SNPS'
