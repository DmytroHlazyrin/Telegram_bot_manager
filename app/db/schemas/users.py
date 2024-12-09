from typing import Optional

from fastapi_users import schemas
from pydantic import field_validator, BaseModel

from app.db.models import UserRole


class UserRead(schemas.BaseUser[int]):
    role: UserRole
    manager_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    pass


class UserRoleUpdate(BaseModel):
    role: UserRole

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, value):
        if isinstance(value, str):
            value = value.upper()
        if value not in UserRole:
            raise ValueError(f"Invalid role: {value}")
        return value
