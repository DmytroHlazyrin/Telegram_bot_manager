import contextlib
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.auth.auth import auth_backend
from app.core.config import settings
from app.db.models import User, UserRole
from app.db.repositories.users import UsersRepository
from app.db.schemas.users import UserCreate
from app.db.session import get_user_db, get_async_session
from app.services.users import UsersService


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(
            self,
            user: User,
            request: Optional[Request] = None
    ) -> None:
        print(f"User {user.id} has registered.")


async def get_user_manager(
        user_db: SQLAlchemyUserDatabase = Depends(get_user_db)
) -> UserManager:
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
        email: str,
        password: str,
        is_superuser: bool = False,
        role: UserRole = UserRole.USER,
        manager_id: Optional[int] = None
) -> User:
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            role=role,
                            manager_id=manager_id,
                        )
                    )
    except UserAlreadyExists:
        print("User already exists.")
        raise
    if role != UserRole.USER:
        await UsersService(UsersRepository).update_user_role(user.id, role)
    if manager_id:
        await UsersService(UsersRepository).assign_manager_to_user(
            user.id, manager_id)
    return user
