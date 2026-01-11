from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserSimple

class GroupMemberCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: UUID
    role: str = "member"

class GroupMemberResponse(BaseModel):
    group_id: UUID
    user_id: UUID
    role: str
    joined_at: datetime

class GroupMemberSimple(BaseModel):
    user: UserSimple = Field(default_factory=dict)
    role: str

    model_config = ConfigDict(from_attributes=True)