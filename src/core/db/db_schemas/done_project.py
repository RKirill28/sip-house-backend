from pydantic import BaseModel, Field

from src.core.db.db_schemas.image import DBImageModel


class DoneProjectModel(BaseModel):
    name: str = Field(max_length=32)
    address: str = Field(max_length=32)
    images: list[DBImageModel]
