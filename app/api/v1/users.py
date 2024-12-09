from typing import List

from fastapi import APIRouter, Depends

from app.auth.dependencies import current_admin_user
from app.auth.manager import current_user
from app.db.schemas.users import UserRead, UserRoleUpdate
from app.db.models import User
from app.db.repositories.users import UsersRepository
from app.services.users import UsersService

router = APIRouter()

@router.get("/users", response_model=List[UserRead])
async def get_users_endpoint(
        current_user: User = Depends(current_user)
) -> List[UserRead]:
    """Retrieve a list of users."""
    return await UsersService(UsersRepository).get_users(current_user)


@router.get("/users/{user_id}", response_model=UserRead)
async def get_user_by_id_endpoint(
        user_id: int,
        current_user: User = Depends(current_user)
) -> UserRead:
    """Retrieve a specific user by ID."""
    return await UsersService(UsersRepository).get_user_by_id(current_user, user_id)


@router.put("/users/{user_id}/role", response_model=UserRead)
async def update_user_role_endpoint(
        user_id: int,
        role_data: UserRoleUpdate,
        current_user: User = Depends(current_admin_user)
) -> UserRead:
    """Update a user's role."""
    return await UsersService(UsersRepository).update_user_role(user_id, role_data.role)

@router.put("/users/{user_id}/assign_manager",
            response_model=UserRead)
async def assign_manager_endpoint(
        user_id: int,
        manager_id: int,
        current_user: User = Depends(current_admin_user)
) -> UserRead:
    return await UsersService(UsersRepository).assign_manager_to_user(user_id, manager_id)
