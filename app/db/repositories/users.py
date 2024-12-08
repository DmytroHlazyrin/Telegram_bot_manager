from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from app.db.models import User
from app.db.session import async_session_maker
from app.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def get_subordinates(self, manager_id: int) -> list:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.manager_id == manager_id)
            result = await session.execute(stmt)
            return result.scalars().all()


    async def assign_manager_to_user(self, user_id: int, manager_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    stmt = (
                        update(self.model)
                        .where(self.model.id == user_id)
                        .values(manager_id=manager_id)
                        .execution_options(synchronize_session="fetch")
                    )
                    await session.execute(stmt)
                    return {"status": "success", "message": f"Manager for user {user_id} updated to {manager_id}"}
                except IntegrityError as e:
                    await session.rollback()
                    return {"status": "error", "message": str(e)}
