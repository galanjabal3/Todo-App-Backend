from typing import Generic, List, TypeVar, Optional, Dict, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    status: str = "200 OK"
    message: str = "Success"
    data: Optional[T] = None


class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int


class ListResponse(BaseResponse[List[T]], Generic[T]):
    data: List[T]


class ListResponseWithPagination(BaseResponse[List[T]], Generic[T]):
    data: List[T]
    pagination: PaginationResponse
    metadata: Dict[str, Any] = Field({})


class BaseFilter(BaseModel):
    id: Optional[int] = Field(default=None)

