from uuid import UUID
from datetime import datetime
from typing import Generic, List, TypeVar, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator

T = TypeVar("T")

class MyBaseModel(BaseModel):
    class Config:
        # Optional: allow arbitrary types if needed
        arbitrary_types_allowed = True

    @field_validator("*", mode="before")
    def format_uuid_and_datetime(cls, v: Any):
        if isinstance(v, UUID):
            return str(v)
        if isinstance(v, datetime):
            return v.isoformat()
        return v

class BaseResponse(BaseModel, Generic[T]):
    code: int = 200
    status: str = "200 OK"
    message: str = "Success"
    data: Optional[T] = None
    
class DeleteResponse(BaseResponse[bool]):
    data: Union[bool, None] = True

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
    
class BasePaginationFilter(BaseModel):
    page: Optional[int] = Field(default=1)
    limit: Optional[int] = Field(default=100)

class BaseFilter(BaseModel):
    id: Optional[int] = Field(default=None)
