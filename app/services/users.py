from fastapi import HTTPException

from app.db.models import User, UserRole
from app.utils.pagination import PaginationParams
from app.utils.repository import AbstractRepository
from fastapi import HTTPException

from app.db.models import User, UserRole
from app.utils.repository import AbstractRepository


class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo = users_repo()

    async def get_users(self, current_user: User, pagination: PaginationParams):
        """Only admin users should be able to see all users.
        Managers should have access to their subordinates."""
        if current_user.role == UserRole.ADMIN:
            return await self.users_repo.get_all(pagination)
        elif current_user.role == UserRole.MANAGER:
            return await self.users_repo.get_subordinates(current_user.id, pagination)
        else:
            raise HTTPException(status_code=403, detail="Only admin and managers can access this resource.")

    async def get_user_by_id(self, current_user: User, user_id: int):
        result = await self.users_repo.get_one(user_id)
        if (current_user.role == UserRole.ADMIN
            or
            (current_user.role == UserRole.MANAGER and
             result.manager_id == current_user.id)
            or
                current_user.id == user_id):
            return result
        raise HTTPException(status_code=403, detail="Only admin and managers can access this resource.")

    async def update_user_role(self, user_id: int, role: UserRole = None):
        result = await self.users_repo.update_one(user_id, {"role": role})
        return result

    async def assign_manager_to_user(self, user_id: int, manager_id: int):
        if user_id == manager_id:
            raise HTTPException(status_code=400, detail="Cannot assign a user as their own manager.")
        # Check if both users exist
        await self.users_repo.get_one(user_id)
        await self.users_repo.get_one(manager_id)
        result = await self.users_repo.update_one(user_id, {"manager_id": manager_id})
        return result

