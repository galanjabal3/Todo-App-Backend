from app.container import ServiceContainer
from app.utils.enums import EntityType

from app.services.user_service import UserService
from app.services.group_service import GroupService
from app.services.group_member_service import GroupMemberService
from app.services.task_service import TaskService


ServiceContainer.register(EntityType.USER, UserService)
ServiceContainer.register(EntityType.GROUP, GroupService)
ServiceContainer.register(EntityType.GROUP_MEMBER, GroupMemberService)
ServiceContainer.register(EntityType.TASK, TaskService)
