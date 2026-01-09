from uuid import UUID
from pydantic import BaseModel, Field

from src.core.schemas.image import ReadImageModel


class CreateProjectModel(BaseModel):
    name: str = Field(max_length=32)
    description: str = Field(max_length=500)
    price: float
    price_description: str = Field(max_length=255)


class ReadProjectModel(CreateProjectModel):
    id: UUID
    pdf_url: str | None
    images: list[ReadImageModel] | None
