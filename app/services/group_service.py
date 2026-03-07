from typing import TYPE_CHECKING
from app.container import ServiceContainer
from app.repositories.group_repository import GroupRepository
from app.services.base import BaseService
from app.schemas.group import GroupResponse, PreviewGroupResponse
from app.utils.logger import logger
from app.utils.enums import EntityType, GroupRole
from app.utils.http_exceptions import not_found, bad_request, forbidden, conflict
from app.utils.token_group import verify_group_invite_token, generate_group_invite_token

if TYPE_CHECKING:
    from app.services.group_member_service import GroupMemberService
    from app.services.user_service import UserService
    from app.services.task_service import TaskService

class GroupService(BaseService[GroupRepository]):
    
    def __init__(self):
        # We pass the repo and the schema variable to the parent
        super().__init__(repository=GroupRepository())
    
    @property
    def group_member_service(self) -> "GroupMemberService":
        return ServiceContainer.get(EntityType.GROUP_MEMBER)

    @property
    def user_service(self) -> "UserService":
        return ServiceContainer.get(EntityType.USER)

    @property
    def task_service(self) -> "TaskService":
        return ServiceContainer.get(EntityType.TASK)

    def get_all_group_by_member(self, user_id: str):
        group_members = self.group_member_service.get_all_with_filters(filters={
            "user_id": user_id,
        }, to_model=True)
        
        if not group_members:
            return []
        
        group_ids = {x.group.id: x for x in group_members}

        return self.get_all_with_filters({"ids": list(group_ids.keys())})
    
    def create_group(self, payload: dict = None, user_id: str = None):
        try:
            # Check User
            user = self.user_service.get_by_id(id=user_id, to_model=True)
            if not user:
                not_found(msg=f"User id '{user_id}' is not found.")
            
            # Make a new group
            new_group = self.repo.create(payload, to_model=True)
            
            # Assign account to admin group member
            self.group_member_service.create({
                "group": new_group,
                "user": user,
                "role": GroupRole.ADMIN.value
            }, to_model=True)
            
            return GroupResponse.model_validate(new_group).model_dump(mode="json")
            
        except Exception as e:
            logger.error(f"Err in create_group: {e}", exc_info=e)
            raise
    
    def delete_group_by_id(self, group_id: str, user_id: str):
        group = self.get_by_id(id=group_id, to_model=True)
        if not group:
            not_found(msg="Group not found")
        
        # Cek apakah user adalah admin
        member = self.group_member_service.get_one_by_filters({
            "group_id": group_id,
            "user_id": user_id,
        }, to_model=True)
        if not member or member.role != "admin":
            forbidden("Only admin can delete group")

        filters = {
            "group_id": group_id
        }
        
        # Delete Member Group & Task
        self.group_member_service.delete_with_filters(filters=filters, soft_delete=False)
        self.task_service.delete_with_filters(filters=filters, soft_delete=False)

        # Delete Group
        self.repo.delete_by_id(id=group_id, soft_delete=False)

        return True


    def get_group_invite_token(self, group_id: str, user_id: str, expires_days: int = 7):
        group = self.get_by_id(id=group_id, to_model=True)
        if not group:
            not_found(msg="Group not found")
        
        # Cek apakah user adalah admin
        member = self.group_member_service.get_one_by_filters({
            "group_id": group_id,
            "user_id": user_id,
        }, to_model=True)
        if not member or member.role != "admin":
            forbidden("Only admin can generate invite link")
        
        token = generate_group_invite_token(group_id, expires_days=expires_days)
        return {
            "link": f"https://taskly-app-lemon.vercel.app/join/{token}",
            # "link": f"localhost:5173/join/{token}",
            "expires_days": expires_days,  # ← info untuk FE
        }

    def preview_group_by_token(self, token: str):
        token_loads = verify_group_invite_token(token=token)
        group_id = token_loads.get("group_id")

        group = self.get_by_id(id=group_id, to_model=True)
        if not group:
            not_found(msg="Group not found")

        result = PreviewGroupResponse.model_validate(group).model_dump(mode="json")
        result["member_count"] = len([m for m in group.members if m.role != "pending"])
        
        return result

    def request_join_group_by_token(self, token: str, user_id: str):
        data = verify_group_invite_token(token)
        group_id = data["group_id"]

        group = self.get_by_id(id=group_id, to_model=True)
        if not group:
            not_found(msg="Group not found")
        
        user = self.user_service.get_by_id(id=user_id, to_model=True)
        if not user:
            not_found(msg="User not found")

        existing = self.group_member_service.get_one_by_filters({
            "group_id": group_id,
            "user_id": user_id,
        }, raise_error=False, to_model=True)

        if existing:
            if existing.role == "pending":
                return {"message": "Already requested"}
            return {"message": "Already joined"}

        self.group_member_service.create({
            "group": group,
            "user": user,
            "role": "pending"
        }, to_model=True)

        return {"message": "Success requested"}
    
    def approve_member(self, group_id: str, user_id: str, admin_id: str, approve: bool = True):
        admin = self.group_member_service.get_one_by_filters({
            "group_id": group_id,
            "user_id": admin_id,
        }, to_model=True)
        if not admin or admin.role != "admin":
            forbidden(msg="Only admin can approve")

        member = self.group_member_service.get_one_by_filters({
            "group_id": group_id,
            "user_id": user_id,
        }, to_model=True)
        if not member:
            not_found(msg="User not found in group")
        if member.role != "pending":
            conflict(msg="User is not pending")

        if approve:
            member.role = "member"
            return {"approved": True, "message": "Member approved"}
        else:
            # Reject — hapus dari group
            member.delete()
            return {"approved": False, "message": "Member rejected"}
    
    def leave_group_by_user(self, group_id: str, user_id: str):
        filters = {
            "group_id": group_id,
            "user_id": user_id,
        }
        member = self.group_member_service.get_one_by_filters(filters, to_model=True)
        if not member:
            not_found(msg="Member not found")

        self.task_service.unassign_tasks_by_user_in_group(group_id=group_id, user_id=user_id)
        
        self.group_member_service.delete_with_filters(filters=filters)

        return True
    
    def remove_members_from_group(self, group_id: str, user_id: str, admin_id: str):
        admin = self.group_member_service.get_one_by_filters({
            "group_id": group_id,
            "user_id": admin_id,
        }, to_model=True)
        if not admin or admin.role != "admin":
            forbidden(msg="Only admin can remove member")

        filters = {
            "group_id": group_id,
            "user_id": user_id,
        }
        member = self.group_member_service.get_one_by_filters(filters, to_model=True)
        if not member:
            not_found(msg="Member not found")

        self.task_service.unassign_tasks_by_user_in_group(group_id=group_id, user_id=user_id)
        
        self.group_member_service.delete_with_filters(filters=filters)

        return True