from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from app.schemas.base import *
from app.schemas.group_member import GroupMemberSimple

class GroupFilter(BasePaginationFilter):
    name: Optional[str] = None

class GroupPayload(BaseModel):
    name: str

class GroupResponse(MyBaseModel):
    id: str
    name: str
    created_at: Optional[str] = None
    members: List[GroupMemberSimple] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)
    
class GroupResponseResource(BaseResponse):
    data: GroupResponse

class ListGroupResponseResource(ListResponseWithPagination):
    data: List[GroupResponse]

class GroupSimple(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)
