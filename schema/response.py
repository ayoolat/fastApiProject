from typing import TypeVar, Generic, List

from pydantic import BaseModel

T = TypeVar('T')


class ResponseDTO(BaseModel, Generic[T]):
    code: int
    body: T
    message: str


class PagedList(BaseModel, Generic[T]):
    data: List[T]
    page: int
    total_count: int