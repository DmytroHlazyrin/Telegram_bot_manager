from abc import ABC, abstractmethod
from typing import Any

from fastapi import HTTPException
from sqlalchemy import insert, select, func

from app.db.session import async_session_maker
from app.utils.pagination import PaginationParams


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, pagination: PaginationParams):
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

    async def add_one(self, data: dict):
        async with async_session_maker() as session:
            query = insert(self.model).values(**data).returning(self.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    async def get_all(self, pagination: PaginationParams = None):
        async with async_session_maker() as session:
            query = select(self.model)
            query = pagination.apply(query, self.model)

            total_query = select(func.count()).select_from(self.model)
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

    async def get_one(self, id: int):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == id)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if result:
                return result
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"No {self.model.__name__} found with id {id}")

    async def update_one(self, id: int, data: dict):
        async with async_session_maker() as session:
            query = self.model.__table__.update().where(
                self.model.id == id).values(**data)
            await session.execute(query)
            await session.commit()
            return await self.get_one(id)

    async def delete_one(self, id: int):
        async with async_session_maker() as session:
            query = self.model.__table__.delete().where(self.model.id == id)
            await session.execute(query)
            await session.commit()


