from sqlalchemy import select

from typing import Sequence
from uuid import UUID

from src.core.schemas import CreateImageModel, UpdateImageModel
from src.core.db.models import Image

from . import BaseRepository


class ImageRepository(BaseRepository[Image, CreateImageModel]):
    model = Image

    async def get_all_by_project_id(self, project_id: UUID) -> Sequence[Image]:
        res = await self.session.execute(
            select(Image).where(Image.project_id == project_id)
        )
        return res.scalars().all()

    async def update_image(self, update_image: UpdateImageModel) -> Image:
        image_obj = await self.session.get_one(Image, update_image.id)
        image_obj.url = update_image.url
        return image_obj
