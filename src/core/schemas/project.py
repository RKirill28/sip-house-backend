from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from src.core.schemas.image import ReadImageModel


class CreateProjectModel(BaseModel):
    name: str = Field(max_length=32)
    description: str = Field(max_length=500)
    price: float
    price_description: str = Field(max_length=255)


class UpdateProjectModel(BaseModel):
    id: UUID
    pdf_urls: list[str]


class ReadProjectModel(CreateProjectModel):
    id: UUID
    images: list[ReadImageModel] | None = None
    pdf_urls: list[str] | None = None

    model_config = {"from_attributes": True}
