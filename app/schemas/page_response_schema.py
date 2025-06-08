from typing import List, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class PageResponseSchema(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_previous: bool
