from src.core.db.repositories import BaseRepository
from src.core.db.models import Image


class ImageRepository(BaseRepository[Image, ImageModel]):
    model = Image
