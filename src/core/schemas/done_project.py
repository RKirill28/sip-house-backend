from pydantic import BaseModel, Field

from core.schemas.image import ImageModel


class DoneProjectModel(BaseModel):
    name: str = Field(max_length=32)
    address: str = Field(max_length=32)
    images: list[ImageModel]
