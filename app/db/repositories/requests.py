from fastapi import HTTPException
from sqlalchemy import select, func

from app.db.session import async_session_maker
from app.utils.repository import SQLAlchemyRepository
from app.db.models import Request, UserRole, User


class RequestsRepository(SQLAlchemyRepository):
    model = Request

    async def get_subordinates_requests(self, manager_id: int, pagination) -> dict:
        """
        Fetches all requests made by subordinates of a specific manager.
        """
        async with async_session_maker() as session:
            query = select(self.model).join(User).where(
                User.manager_id == manager_id
            )
            query = pagination.apply(query, self.model)

            total_query = select(func.count()).select_from(self.model).join(User).where(
                User.manager_id == manager_id)
            total = (await session.execute(total_query)).scalar()

            result = await session.execute(query)
            items = result.scalars().all()

            return {
                "items": items,
                "total": total,
                "page": pagination.page,
                "page_size": pagination.page_size,
                "pages": (total + pagination.page_size - 1) // pagination.page_size,
            }

    async def get_users_requests(self, user_id: int, pagination) -> dict:
        """
        Fetches all requests made by a specific user.
        """
        async with async_session_maker() as session:
            query = select(self.model).where(
                self.model.author_id == user_id)
            query = pagination.apply(query, self.model)

            total_query = select(func.count()).select_from(self.model).where(
                self.model.author_id == user_id)
            total = (await session.execute(total_query)).scalar()

            result = await session.execute(query)
            items = result.scalars().all()

            return {
                "items": items,
                "total": total,
                "page": pagination.page,
                "page_size": pagination.page_size,
                "pages": (total + pagination.page_size - 1) // pagination.page_size,
            }

