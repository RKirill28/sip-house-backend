from pydantic import BaseModel, Field

from src.core.schemas.image import ImageModel


class ProjectModel(BaseModel):
    name: str = Field(max_length=32)
    desctiption: str = Field(max_length=500)
    price: int
    price_description: str = Field(max_length=255)
    # pdf file
    images: list[ImageModel]
