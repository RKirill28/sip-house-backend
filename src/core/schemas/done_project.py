from pydantic import BaseModel, Field

from src.core.schemas.image import ReadImageModel


class DoneProjectModel(BaseModel):
    name: str = Field(max_length=32)
    address: str = Field(max_length=32)
    images: list[ReadImageModel]
