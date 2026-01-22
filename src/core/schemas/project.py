from uuid import UUID
from pydantic import Field

from src.core.schemas.base import MyBaseModel
from src.core.schemas.image import ReadImageModel


class CreateProjectModel(MyBaseModel):
    name: str = Field(max_length=32)
    description: str = Field(max_length=500)
    price: float
    price_description: str = Field(max_length=255, alias="priceDescription")


class UpdateProjectPdfUrlModel(MyBaseModel):
    id: UUID
    pdf_urls: list[str] = Field(alias="pdfUrls")


class UpdateProjectModel(MyBaseModel):
    name: str | None = Field(None, max_length=32)
    description: str | None = Field(None, max_length=500)
    price: float | None = None
    price_description: str | None = Field(
        None, max_length=255, alias="priceDescription"
    )
    public: bool


class ReadProjectModel(CreateProjectModel):
    id: UUID
    images: list[ReadImageModel] | None = None
    pdf_urls: list[str] | None = Field(default=None, alias="pdfUrls")
    public: bool


class ReadAllProjectsModel(MyBaseModel):
    items: list[ReadProjectModel]
    count: int
