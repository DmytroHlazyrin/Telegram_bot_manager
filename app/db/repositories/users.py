from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError

from app.db.models import User
from app.db.session import async_session_maker
from app.utils.pagination import PaginationParams
from app.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def get_subordinates(
            self, manager_id: int, pagination: PaginationParams
    ) -> dict:
        async with async_session_maker() as session:
            query = select(self.model).where(
                self.model.manager_id == manager_id
            )
            query = pagination.apply(query, self.model)

            total_query = select(func.count()).select_from(self.model).where(
                self.model.manager_id == manager_id
            )
            total = (await session.execute(total_query)).scalar()

            result = await session.execute(query)
            items = result.scalars().all()

            return {
                "items": items,
                "total": total,
                "page": pagination.page,
                "page_size": pagination.page_size,
                "pages": ((total + pagination.page_size - 1)
                          // pagination.page_size),
            }


    async def assign_manager_to_user(
            self, user_id: int, manager_id: int
    ) -> dict:
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    query = (
                        update(self.model)
                        .where(self.model.id == user_id)
                        .values(manager_id=manager_id)
                        .execution_options(synchronize_session="fetch")
                    )
                    await session.execute(query)
                    return {
                        "status": "success",
                        "message": f"Manager for user {user_id} "
                                   f"updated to {manager_id}"
                    }
                except IntegrityError as e:
                    await session.rollback()
                    return {"status": "error", "message": str(e)}
