from core.db.models import Image
from core.schemas import ImageModel
from . import BaseRepository


class ImageRepository(BaseRepository[Image, ImageModel]):
    model = Image
