from enum import Enum
import strawberry
from typing import List, Optional

@strawberry.input (
        description="Specifies the record number to start from and the maximum number of records to output"
)
class PageArgs:
    from_: Optional[int] = 0
    size: Optional[int] = 50 
    
@strawberry.input(
        description="specifies list of attributes that should not be null for a record to be returned"
)
class FilterArgs:
    exists:  Optional[List[str]] = None
    # many more will come as needed so this will be updated as needed and flexible

@strawberry.type
class Bucket:
    key: str
    doc_count: int

@strawberry.type
class DocCount:
    doc_count: int = strawberry.field(description ="The number of records from the operation")

@strawberry.input
class Histogram:
    interval: Optional[float] = 4893.27
    min: Optional[int] = 10636
    max: Optional[int] = 499963

@strawberry.type
class AggregationItem:    
    doc_count: int
    min: Optional[float] = None
    max: Optional[float] = None
    histogram: Optional[list[Bucket]] = None
    frequency: Optional[list[Bucket]] = None
    missing: Optional[DocCount] = None


class QueryType(Enum):
    DOWNLOAD = 'DOWNLOAD'
    SNPS = 'SNPS'
    AGGS = 'AGGS'
    SCROLL = 'SCROLL'

@strawberry.enum
class QueryTypeOption(Enum):
    SNPS = 'SNPS'
    SCROLL = 'SCROLL'

