from sqlalchemy import select

from typing import Sequence
from uuid import UUID

from src.core.schemas.image import CreateImageInDBModel
from src.core.db.models import Image, Project

from . import BaseRepository


class ImageRepository(BaseRepository[Image, CreateImageInDBModel]):
    model = Image

    async def get_all_by_project_id(self, project_id: UUID) -> Sequence[Image]:
        res = await self.session.execute(
            select(Image).where(Image.project_id == project_id)
        )
        return res.scalars().all()
