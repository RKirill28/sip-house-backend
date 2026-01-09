from pydantic import BaseModel, Field

from fastapi import UploadFile, File

from uuid import UUID


class CreateImageModel(BaseModel):
    """For API"""

    project_id: UUID
    # url: str
    name: str = Field(max_length=32)
    description: str = Field(max_length=255)
    main_image: bool
    sort: int
    done_project_id: UUID | None = None


class CreateImageForm(CreateImageModel):
    image_file: UploadFile = File(media_type="image/png")


class CreateImageInDBModel(CreateImageModel):
    """For save in DB"""

    url: str


class ReadImageModel(CreateImageModel):
    url: str
