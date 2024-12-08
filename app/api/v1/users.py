from typing import List

from fastapi import APIRouter, Depends

from app.auth.manager import current_user
from app.auth.schemas import UserRead
from app.db.models import User
from app.db.repositories.users import UsersRepository
from app.services.users import UsersService

router = APIRouter()

@router.get("/users", response_model=List[UserRead])
async def get_users_endpoint(
        current_user: User = Depends(current_user)
):
    """Retrieve a list of users."""
    return await UsersService(UsersRepository).get_users(current_user)
