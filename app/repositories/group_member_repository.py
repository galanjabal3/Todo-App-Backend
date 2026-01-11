from app.schemas.group_member import *
from app.repositories.base import BaseRepository
from app.db.models import GroupMemberDB

class GroupMemberRepository(BaseRepository):
    entity = GroupMemberDB
    
    # Mapping filter fields:
    # q = Query object, v = Value input, t = Table entity
    filter_map = {
        "role": lambda x, v: x.filter(lambda t: t.role.lower() == v),
    }
    
    def __init__(self):
        # We pass the repo and the schema variable to the parent
        super().__init__(schema_class=GroupMemberResponse)