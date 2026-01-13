from pydantic import Field

from fastapi import UploadFile, File

from uuid import UUID

from src.core.schemas.base import MyBaseModel


class CreateImageModel(MyBaseModel):
    """For API"""

    project_id: UUID = Field(alias="projectId")
    name: str = Field(max_length=32)
    description: str = Field(max_length=255)
    main_image: bool = Field(alias="mainImage")
    sort: int
    done_project_id: UUID | None = Field(default=None, alias="doneProjectId")


class CreateImageForm(CreateImageModel):
    image_file: UploadFile = File(media_type="image/png", alias="imageFile")


class CreateImageInDBModel(CreateImageModel):
    """For save in DB"""

    url: str


class ReadImageModel(CreateImageModel):
    id: UUID
    url: str | None


class UpdateImageModel(MyBaseModel):
    id: UUID
    url: str
