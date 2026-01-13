from pathlib import Path
from sqlalchemy import select

from typing import Sequence, override
from uuid import UUID

from src.core.enums import ImageSortBy
from src.core.schemas import CreateImageModel, UpdateImageUrlModel
from src.core.db.models import Image

from src.core.conifg import settings

from . import BaseRepository


class ImageRepository(BaseRepository[Image, CreateImageModel, ImageSortBy]):
    model = Image

    async def get_all_by_project_id(self, project_id: UUID) -> Sequence[Image]:
        res = await self.session.execute(
            select(Image).where(Image.project_id == project_id)
        )
        return res.scalars().all()

    async def update(self, update_image_url: UpdateImageUrlModel) -> Image:
        image_obj = await self.get_by_id(update_image_url.id)
        image_obj.url = update_image_url.url
        return image_obj

    @override
    async def remove(self, id: UUID) -> None:
        image = await self.get_by_id(id)
        path = image.url
        if path:
            path = Path(path)
            path = settings.BASE_DIR / path
            if path.is_file():
                path.unlink()

        await self.session.delete(image)
