from app.schemas.user import *
from app.repositories.base import BaseRepository
from app.db.models import UserDB

class UserRepository(BaseRepository):
    entity = UserDB
    
    # Mapping filter fields:
    # q = Query object, v = Value input, t = Table entity
    filter_map = {
        **BaseRepository.filter_map,
        "email": lambda x, v: x.filter(lambda t: t.email == v),
        "username": lambda x, v: x.filter(lambda t: t.username == v),
    }
    
    def __init__(self):
        # We pass the repo and the schema variable to the parent
        super().__init__(schema_class=UserPublicResponse)
    