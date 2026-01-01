from app.services.base import BaseService
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserResponse

class UserService(BaseService):
    def __init__(self):
        # We pass the repo and the schema variable to the parent
        super().__init__(repository=UserRepository(), schema_class=UserResponse)
    