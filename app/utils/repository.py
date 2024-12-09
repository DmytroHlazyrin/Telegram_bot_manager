from abc import ABC, abstractmethod

from fastapi import HTTPException
from sqlalchemy import insert, select

from app.db.session import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> int:
        async with async_session_maker() as session:
            query = insert(self.model).values(**data).returning(self.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def get_all(self):
        async with async_session_maker() as session:
            query = select(self.model)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_one(self, id: int) -> dict:
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if result:
                return result
            else:
                raise HTTPException(status_code=404, detail=f"No {self.model.__name__} found with id {id}")

    async def update_one(self, id: int, data: dict):
        async with async_session_maker() as session:
            query = self.model.__table__.update().where(self.model.id == id).values(**data)
            await session.execute(query)
            await session.commit()
            return await self.get_one(id)

    async def delete_one(self, id: int):
        async with async_session_maker() as session:
            query = self.model.__table__.delete().where(self.model.id == id)
            await session.execute(query)
            await session.commit()


