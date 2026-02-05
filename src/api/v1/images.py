from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from src.infra.db.repositories.base import NoEntityByIdFound
from src.core.schemas import (
    CreateImageModel,
    ReadImageModel,
    UpdateImageModel,
    UpdateImageUrlModel,
)
from src.core.conifg import settings

from src.api.deps import (
    AdminDap,
    FileWorkerServiceDap,
    ImageRepoDap,
)


images_router = APIRouter(prefix=settings.api.v1.images_prefix)


@images_router.post("", response_model=ReadImageModel)
async def create(image_repo: ImageRepoDap, create_image: CreateImageModel, _: AdminDap):
    if create_image.done_project_id and create_image.project_id:
        raise HTTPException(433, "You can specify either project_id or done_project_id")
    elif create_image.done_project_id is None and create_image.project_id is None:
        raise HTTPException(
            433, "Specify either project_id or done_project_id, one of the two required"
        )
    else:
        try:
            if create_image.main_image:
                curr_images = await image_repo.get_all_by_project_id(
                    create_image.project_id
                )
                for image in curr_images:
                    image.main_image = False

            new = await image_repo.create(create_image)
            await image_repo.session.commit()
            return new
        except IntegrityError:
            raise HTTPException(404, "No done_project/project found by id")


@images_router.put("/add_image_urls", response_model=list[ReadImageModel])
async def add_image_urls(
    image_repo: ImageRepoDap, update_model: list[UpdateImageUrlModel], _: AdminDap
):
    res = []
    for model in update_model:
        try:
            res.append(await image_repo.update_image_url(model))
        except NoEntityByIdFound:
            raise HTTPException(404, "No image found by id")

    await image_repo.session.commit()
    return res


@images_router.delete("/{image_id}")
async def delete_by_id(
    image_repo: ImageRepoDap,
    file_worker: FileWorkerServiceDap,
    image_id: UUID,
    _: AdminDap,
):
    try:
        image = await image_repo.remove(image_id)
        await image_repo.session.commit()

        if image.url:
            file_worker.remove(image.url)
        else:
            HTTPException(404, "No image url found")

        return {"success": True}
    except NoEntityByIdFound:
        raise HTTPException(404, "No image found by id")


@images_router.get("/{project_id}", response_model=list[ReadImageModel])
async def get_by_project_id(image_repo: ImageRepoDap, project_id: UUID):
    return await image_repo.get_all_by_project_id(project_id)


@images_router.put("/{image_id}")
async def update(
    image_repo: ImageRepoDap,
    image_id: UUID,
    update_model: UpdateImageModel,
    _: AdminDap,
):
    try:
        image = await image_repo.get_by_id(image_id)
    except NoEntityByIdFound:
        raise HTTPException(404, "No image found by id")

    if image.main_image:
        if image.project_id is not None:
            images = await image_repo.get_all_by_project_id(image.project_id)
        elif image.done_project_id is not None:
            images = await image_repo.get_all_by_done_project_id(image.done_project_id)
        else:
            raise HTTPException(404, "No project_id or done_project_id")

        for db_img in images:
            db_img.main_image = False

        image.main_image = True

    await image_repo.update(image_id, update_model)
    await image_repo.session.commit()
    return {"success": True}
