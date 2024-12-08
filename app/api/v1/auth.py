from fastapi import APIRouter


from app.auth.auth import auth_backend
from app.auth.manager import fastapi_users
from app.auth.schemas import UserRead, UserCreate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
)

