import uuid
from datetime import datetime, timezone
from pony.orm import Required, Optional, PrimaryKey
from app.db.database import dbcon

db = dbcon()

class UserDB(db.Entity):
    _table_ = "users"
    id = PrimaryKey(uuid.UUID, default=uuid.uuid4)
    email = Required(str, unique=True)
    username = Optional(str, unique=True, nullable=True)
    password = Required(str)
    full_name = Required(str)
    created_at = Required(datetime, default=lambda: datetime.now(timezone.utc))
    updated_at = Optional(datetime, default=lambda: datetime.now(timezone.utc))
    is_deleted = Required(bool, default=False)
