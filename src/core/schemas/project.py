from pydantic import BaseModel, Field, FileUrl

from src.core.schemas import ImageModel


class ProjectModel(BaseModel):
    name: str = Field(max_length=32)
    desctiption: str = Field(max_length=500)
    price: int
    price_description: str = Field(max_length=255)
    pdf_url: FileUrl | None = None
    images: list[ImageModel] | None = None
