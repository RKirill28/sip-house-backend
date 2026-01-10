from typing import Type, Sequence
from uuid import UUID
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.db.models import Base


class BaseRepository[T: Base, P: BaseModel]:
    model: Type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, scheme: P) -> T:
        new = self.model(**scheme.model_dump())
        self.session.add(new)
        await self.session.flush()
        await self.session.refresh(new)
        return new

    async def get_by_id(self, id: UUID) -> T | None:
        return await self.session.get(self.model, id)

    async def get_all(self) -> Sequence[T]:
        res = await self.session.execute(select(self.model))
        return res.scalars().all()

    async def remove(self, id: int) -> None:
        obj = await self.session.get(self.model, id)
        if obj:
            await self.session.delete(obj)
