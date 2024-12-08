from typing import Optional

from fastapi_users import schemas
from app.db.models import UserRole


class UserRead(schemas.BaseUser[int]):
    role: UserRole
    manager_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    pass
