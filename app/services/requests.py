from fastapi import HTTPException

from app.db.models import User, UserRole
from app.utils.pagination import PaginationParams
from app.utils.repository import AbstractRepository


class RequestsService:
    def __init__(self, requests_repo: AbstractRepository):
        self.requests_repo = requests_repo()

    async def get_requests(self, current_user: User, pagination: PaginationParams):
        """Only admin users should be able to see all users messages.
        Managers should have access to their subordinates messages.
        Users should only have access to their own messages."""
        if current_user.role == UserRole.ADMIN:
            return await self.requests_repo.get_all(pagination)
        elif current_user.role == UserRole.MANAGER:
            return await self.requests_repo.get_subordinates_requests(current_user.id, pagination)
        elif current_user.role == UserRole.USER:
            return await self.requests_repo.get_users_requests(current_user.id, pagination)
        else:
            raise HTTPException(status_code=403, detail="Only admin and managers can access this resource.")

    # async def get_user_by_id(self, current_user: User, user_id: int):
    #     result = await self.users_repo.get_one(user_id)
    #     if (current_user.role == UserRole.ADMIN
    #         or
    #         (current_user.role == UserRole.MANAGER and
    #          result["manager_id"] == current_user.id)
    #         or
    #             current_user.id == user_id):
    #         return result
    #     raise HTTPException(status_code=403, detail="Only admin and managers can access this resource.")
