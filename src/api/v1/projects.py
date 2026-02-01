from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query

from src.core.conifg import settings
from src.core.db.repositories.base import NoEntityByIdFound
from src.core.schemas import (
    CreateProjectModel,
    ReadProjectModel,
    UpdateProjectPdfUrlModel,
    UpdateProjectModel,
)

from src.api.deps import (
    AdminDap,
    AllProjectParamsDap,
    FileWorkerServiceDap,
    OptionalAdminDap,
    ProjectRepoDap,
)
from src.core.schemas import ReadAllProjectsModel


projects_router = APIRouter(prefix=settings.api.v1.projects_prefix)


@projects_router.post("", response_model=ReadProjectModel)
async def create(
    project_repo: ProjectRepoDap,
    create_project: CreateProjectModel,
    _: AdminDap,
):
    new = await project_repo.create(create_project)
    await project_repo.session.commit()
    return new


@projects_router.get("", response_model=ReadAllProjectsModel)
async def get_all(
    project_repo: ProjectRepoDap,
    params: AllProjectParamsDap,
    admin_dap: OptionalAdminDap,
):
    filters = {}
    if not admin_dap:
        filters["public"] = True

    projects, count = await project_repo.get_all(
        params["offset"],
        params["limit"],
        params["sort_by"],
        params["is_desc"],
        **filters,
    )
    items = [ReadProjectModel.model_validate(p) for p in projects]

    return ReadAllProjectsModel(items=items, count=count)


@projects_router.put("/add_pdf_urls", response_model=ReadProjectModel)
async def add_pdf_urls(
    project_repo: ProjectRepoDap,
    update_model: UpdateProjectPdfUrlModel,
    _: AdminDap,
):
    try:
        project = await project_repo.update_pdf_url(update_model)
        await project_repo.session.commit()

        return project
    except NoEntityByIdFound:
        raise HTTPException(404, "No project found by id.")


@projects_router.get("/random", response_model=list[ReadProjectModel])
async def get_random(project_repo: ProjectRepoDap, limit: int = Query(5)):
    return await project_repo.get_random(limit, public=True)


@projects_router.put("/{project_id}", response_model=ReadProjectModel)
async def update(
    project_repo: ProjectRepoDap,
    project_id: UUID,
    update_model: UpdateProjectModel,
    _: AdminDap,
):
    try:
        res = await project_repo.update(project_id, update_model)
        await project_repo.session.commit()
        return res
    except NoEntityByIdFound:
        raise HTTPException(404, "No project found by id.")


@projects_router.delete("/{project_id}")
async def delete(
    project_repo: ProjectRepoDap,
    file_worker: FileWorkerServiceDap,
    project_id: UUID,
    _: AdminDap,
):
    try:
        project = await project_repo.get_by_id(project_id)
        image_files: list[str] = [image.url for image in project.images]
        await project_repo.remove(project_id)
        await project_repo.session.commit()

        for file in image_files:
            file_worker.remove(file)

        return {"success": True}
    except NoEntityByIdFound:
        raise HTTPException(404, "No project found by id.")


@projects_router.get("/{project_id}", response_model=ReadProjectModel)
async def get_by_id(project_repo: ProjectRepoDap, project_id: UUID):
    try:
        project = await project_repo.get_by_id(project_id)
        return project
    except NoEntityByIdFound:
        raise HTTPException(404, "No project found by id.")
