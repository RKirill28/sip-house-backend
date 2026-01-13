from uuid import UUID
from fastapi import APIRouter, HTTPException

from src.core.db.repositories.base import NoEntityByIdFound
from src.core.schemas import (
    CreateImageModel,
    ReadImageModel,
    UpdateImageUrlModel,
)
from src.core.conifg import settings

from src.api.deps import ImageRepoDap


images_router = APIRouter(prefix=settings.api.v1.images_prefix)


@images_router.post("/image", response_model=ReadImageModel)
async def create_image(image_repo: ImageRepoDap, create_image: CreateImageModel):
    new = await image_repo.create(create_image)
    return new


@images_router.get("/{project_id}", response_model=list[ReadImageModel])
async def get_images(image_repo: ImageRepoDap, project_id: UUID):
    return await image_repo.get_all_by_project_id(project_id)


@images_router.post("/add_image_urls", response_model=list[ReadImageModel])
async def add_image_ulrs(
    image_repo: ImageRepoDap, update_model: list[UpdateImageUrlModel]
):
    res = []
    for model in update_model:
        try:
            res.append(await image_repo.update(model))
        except NoEntityByIdFound:
            raise HTTPException(404, "No image found by id.")

    await image_repo.session.commit()

    return res


@images_router.put("/image/{image_id}")
async def delete_image_by_id(image_repo: ImageRepoDap, image_id: UUID):
    try:
        await image_repo.remove(image_id)
        return {"success": True}
    except NoEntityByIdFound:
        raise HTTPException(404, "No image found by id.")
