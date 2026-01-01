from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from datetime import datetime, timezone, time
from typing import Optional, List
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    # password: str
    full_name: str
    created_at: str = None
    updated_at: Optional[str] = None
    is_deleted: bool = False

    model_config = ConfigDict(from_attributes=True)

    @field_validator("id", mode="before")
    def format_uuid(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v 
    
    @field_validator("created_at", "updated_at", mode="before")
    def format_datetime(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

class UserResponseSpecTree(BaseModel):
    success: bool
    message: str
    data: List[UserResponse]