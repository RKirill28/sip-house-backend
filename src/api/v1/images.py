from uuid import UUID
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from src.core.schemas.image import (
    CreateImageModel,
    CreateImageInDBModel,
    CreateImageForm,
    ReadImageModel,
)
from src.core.conifg import settings
from src.api.deps import ImageRepoDap, ProjectRepoDap

from src.services import ImageValidationError
from src.usecases.image import CreateImage


images_router = APIRouter(prefix=settings.api.v1.images_prefix)


@images_router.get("/uploads/{project_id}/{image_filename}")
async def get_image_by_url(project_id: UUID, image_filename: str) -> bytes:
    with open(f'')


@images_router.get("/{project_id}", response_model=list[ReadImageModel])
async def get_images(image_repo: ImageRepoDap, project_id: UUID):
    return await image_repo.get_all_by_project_id(project_id)


@images_router.post("/image", response_model=CreateImageInDBModel)
async def create_image(
    image_repo: ImageRepoDap,
    create_image: CreateImageForm = Form(media_type="multipart/form-data"),
):
    try:
        return await CreateImage(image_repo).execute(create_image)
    except ImageValidationError:
        raise HTTPException(
                422, "The file validation error: This file is not allowed."
            )
