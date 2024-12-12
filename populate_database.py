import asyncio
from datetime import datetime
from app.auth.manager import create_user
from app.db.models import UserRole, Request
from app.db.session import async_session_maker


async def create_request(user_id, bot_token, chat_id, message,
                         telegram_response):
    async with async_session_maker() as session:
        request = Request(
            bot_token=bot_token,
            chat_id=chat_id,
            message=message,
            telegram_response=telegram_response,
            author_id=user_id,
            timestamp=datetime.now()
        )
        session.add(request)
        await session.commit()
        return request


async def main():
    users = [
        {"email": "admin@example.com", "role": UserRole.ADMIN, "manager_id": None},
        {"email": "manager1@example.com", "role": UserRole.MANAGER, "manager_id": None},
        {"email": "manager2@example.com", "role": UserRole.MANAGER, "manager_id": None},
        {"email": "user1@example.com", "role": UserRole.USER, "manager_id": 2},
        {"email": "user2@example.com", "role": UserRole.USER, "manager_id": 2},
        {"email": "user3@example.com", "role": UserRole.USER, "manager_id": 3},
    ]

    bot_token = "123456789:TEST_BOT_TOKEN"
    chat_id_base = 100000000

    # Create users
    for i, user_data in enumerate(users):
        user = await create_user(
            email=user_data["email"],
            password="string",
            is_superuser=(user_data["role"] == UserRole.ADMIN),
            role=user_data["role"],
            manager_id=user_data["manager_id"]
        )
        print(f"User created: {user.email}, Role: {user_data['role']}")

        if user_data["role"] == UserRole.USER:
            # Create 4 requests for each user
            for j in range(4):
                message = f"Request {j + 1} from {user.email}"
                telegram_response = {
                    "message": message,
                    "user": user.email,
                    "chat_id": chat_id_base + i * 10 + j
                }
                request = await create_request(
                    user_id=user.id,
                    bot_token=bot_token,
                    chat_id=chat_id_base + i * 10 + j,
                    message=message,
                    telegram_response=telegram_response
                )
                print(f"Created request {request.id} for user {user.email}")


if __name__ == "__main__":
    asyncio.run(main())
