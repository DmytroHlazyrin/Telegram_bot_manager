from fastapi import Depends, HTTPException, status

from app.auth.manager import current_user
from app.db.models import User, UserRole


def current_manager_user(user: User = Depends(current_user)) -> User:
    if user.role != UserRole.MANAGER or user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager privileges required")
    return user


def current_admin_user(user: User = Depends(current_user)) -> User:
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return user

