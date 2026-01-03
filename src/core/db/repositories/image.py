from src.core.db.db_schemas import DBImageModel
from src.core.db.repositories import BaseRepository
from src.core.db.models import Image


class ImageRepository(BaseRepository[Image, DBImageModel]):
    model = Image
