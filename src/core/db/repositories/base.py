from typing import Type, Sequence, Generic, TypeVar, Optional
from uuid import UUID
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from src.core.db.models import Base
from src.core.enums import SortBy

T = TypeVar("T", bound=Base)
P = TypeVar("P", bound=BaseModel)
S = TypeVar("S", bound=SortBy)


class BaseRepository(Generic[T, P, S]):
    model: Type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, scheme: P) -> T:
        new = self.model(**scheme.model_dump())
        self.session.add(new)
        await self.session.flush()
        await self.session.refresh(new)
        return new

    async def get_by_id(self, id: UUID) -> Optional[T]:
        return await self.session.get(self.model, id)

    async def get_all(
        self, offset: int, limit: int, sort_by: S, is_desc: bool
    ) -> tuple[Sequence[T], int]:
        if is_desc:
            sort_by_param = desc(sort_by.project_attr)
        else:
            sort_by_param = sort_by.project_attr

        res = await self.session.execute(
            select(self.model).order_by(sort_by_param).offset(offset).limit(limit)
        )
        count = await self.session.execute(select(self.model.id))

        return (res.scalars().all(), len(count.scalars().all()))

    async def remove(self, id: int) -> None:
        obj = await self.session.get(self.model, id)
        if obj:
            await self.session.delete(obj)
