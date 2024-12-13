from typing import List

from fastapi import HTTPException

from app.db.models import User, UserRole, Request
from app.db.repositories.users import UsersRepository
from app.utils.pagination import PaginationParams
from app.utils.repository import AbstractRepository


class RequestsService:
    def __init__(self, requests_repo: AbstractRepository) -> None:
        self.requests_repo = requests_repo()

    async def get_requests(
            self, current_user: User, pagination: PaginationParams
    ) -> List[Request]:
        """Only admin users should be able to see all users messages.
        Managers should have access to their subordinates messages.
        Users should only have access to their own messages."""
        if current_user.role == UserRole.ADMIN:
            response = await self.requests_repo.get_all(pagination)
        elif current_user.role == UserRole.MANAGER:
            response = await self.requests_repo.get_subordinates_requests(
                current_user.id, pagination)
        elif current_user.role == UserRole.USER:
            response = await self.requests_repo.get_user_requests(
                current_user.id, pagination)
        else:
            raise HTTPException(
                status_code=403,
                detail="Only admin and managers can access this resource.")
        return response

    async def get_user_requests(
            self,
            current_user: User,
            user_id: int,
            pagination: PaginationParams
    ) -> List[Request]:

        if current_user.id == user_id:
            response = await self.requests_repo.get_user_requests(
                user_id, pagination)

        elif current_user.role == UserRole.ADMIN:
            response = await self.requests_repo.get_user_requests(
                user_id, pagination)

        elif current_user.role == UserRole.MANAGER:
            user = await UsersRepository().get_one(user_id)

            if user.manager_id != current_user.id:
                raise HTTPException(status_code=403,
                                    detail="User is not a subordinate.")

            response = await self.requests_repo.get_user_requests(
                user_id, pagination)

        else:
            raise HTTPException(
                status_code=403,
                detail="Only admin and managers can access this resource."
            )

        return response
