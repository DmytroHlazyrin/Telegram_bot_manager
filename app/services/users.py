from app.db.models import User, UserRole
from app.utils.repository import AbstractRepository

class UsersService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo = users_repo()

    async def get_users(self, current_user: User):
        """Only admin users should be able to see all users.
        Managers should have access to their subordinates."""
        if current_user.role == UserRole.ADMIN:
            return await self.users_repo.get_all()
        elif current_user.role == UserRole.MANAGER:
            return await self.users_repo.get_subordinates(current_user.id)
        else:
            raise Exception("Only admin and managers can access this resource.")

    async def get_user_by_id(self, current_user: User, user_id: int):
        result = await self.users_repo.get_one(user_id)
        if (current_user.role == "admin"
            or
            (current_user.role == "manager" and
             result["manager_id"] == current_user.id)
            or
                current_user.id == user_id):
            return result

    async def update_user_role(self, user_id: int, role: str):
        result = await self.users_repo.update_one(user_id, {"role": role})
        return result

