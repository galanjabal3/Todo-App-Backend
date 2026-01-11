from typing import TYPE_CHECKING
from app.container import ServiceContainer
from app.repositories.group_repository import GroupRepository
from app.services.base import BaseService
from app.utils.logger import logger
from app.utils.enums import EntityType
from app.utils.http_exceptions import not_found, conflict

if TYPE_CHECKING:
    from app.services.group_member_service import GroupMemberService

class GroupService(BaseService[GroupRepository]):
    
    def __init__(self):
        # We pass the repo and the schema variable to the parent
        super().__init__(repository=GroupRepository())
    
    @property
    def group_member_service(self) -> "GroupMemberService":
        return ServiceContainer.get(EntityType.GROUP_MEMBER)
    
    def create_group(self, payload: dict = None):
        pass