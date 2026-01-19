from sqlalchemy import select

from typing import Sequence

from uuid import UUID

from src.core.sort_by_enums import ImageSortBy
from src.core.schemas import CreateImageModel, UpdateImageUrlModel
from src.core.db.models import Image

from . import BaseRepository


class ImageRepository(BaseRepository[Image, CreateImageModel, ImageSortBy]):
    model = Image

    async def get_all_by_project_id(self, project_id: UUID) -> Sequence[Image]:
        res = await self.session.execute(
            select(Image).where(Image.project_id == project_id)
        )
        return res.scalars().all()

    async def update_image_url(self, update_image_url: UpdateImageUrlModel) -> Image:
        image_obj = await self.get_by_id(update_image_url.id)
        image_obj.url = update_image_url.url
        return image_obj
