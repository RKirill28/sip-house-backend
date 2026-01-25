from uuid import UUID
from pydantic import Field

from src.core.schemas.base import MyBaseModel
from src.core.schemas.image import ReadImageModel


class CreateDoneProjectModel(MyBaseModel):
    name: str = Field(max_length=32)
    address: str = Field(max_length=32)


class ReadDoneProjectModel(CreateDoneProjectModel):
    id: UUID
    images: list[ReadImageModel]
    public: bool


class UpdateDoneProjectModel(CreateDoneProjectModel):
    public: bool


class ReadAllDoneProjectsModel(MyBaseModel):
    items: list[ReadDoneProjectModel]
    count: int
