from typing import Type, Sequence, Generic, TypeVar
from uuid import UUID
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, desc

from src.core.db.models import Base
from src.core.sort_by_enums import SortBy
from src.core.schemas.base import MyBaseModel

T = TypeVar("T", bound=Base)
P = TypeVar("P", bound=BaseModel)
S = TypeVar("S", bound=SortBy)


class NoEntityByIdFound(Exception):
    pass


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

    async def get_by_id(self, id: UUID) -> T:
        res = await self.session.get(self.model, id)
        if res is None:
            raise NoEntityByIdFound
        return res

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
        count = await self.session.execute(select(func.count()).select_from(self.model))

        return (res.scalars().all(), count.scalar_one())

    async def update(self, entity_id: UUID, update_model: MyBaseModel) -> T:
        entity = await self.get_by_id(entity_id)
        update_model_dict = update_model.model_dump()
        for k, _ in entity.__dict__.items():
            if (new_v := update_model_dict.get(k)) is not None:
                setattr(entity, k, new_v)

        return entity

    async def remove(self, id: UUID) -> T:
        obj = await self.get_by_id(id)
        await self.session.delete(obj)
        return obj
