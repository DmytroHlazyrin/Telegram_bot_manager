import asyncio

from app.auth.manager import create_user
from app.db.models import UserRole


async def main():
    email = "admin@example.com"
    password = "string"
    is_superuser = True
    role = UserRole.ADMIN

    user = await create_user(email=email, password=password, is_superuser=is_superuser, role=role)
    print(f"User created: {user.email}")

if __name__ == "__main__":
    asyncio.run(main())
