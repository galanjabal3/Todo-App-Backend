from datetime import datetime
from pydantic import ConfigDict
from app.schemas.base import MyBaseModel
from app.schemas.user import UserSimple

class GroupMemberCreate(MyBaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    group_id: str
    user_id: str
    role: str = "member"

class GroupMemberResponse(MyBaseModel):
    group: str
    user: str
    role: str
    joined_at: datetime

class GroupMemberSimple(UserSimple):
    role: str
