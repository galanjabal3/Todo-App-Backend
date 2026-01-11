from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.group import GroupSimple
from app.schemas.user import UserSimple

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    due_date: Optional[datetime] = None
    group_id: Optional[UUID] = None
    assigned_to_id: Optional[UUID] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    assigned_to_id: Optional[UUID] = None
    attachment: Optional[list] = []

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    due_date: Optional[datetime]
    assigned_to: UserSimple | None
    group: GroupSimple | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

