from uuid import UUID
from fastapi import APIRouter, HTTPException, Query

from src.core.conifg import settings

from src.api.deps import (
    AdminDap,
    DoneProjectRepoDap,
    AllDoneProjectParamsDap,
    FileWorkerServiceDap,
    OptionalAdminDap,
)
from src.core.db.repositories.base import NoEntityByIdFound
from src.core.schemas import (
    ReadDoneProjectModel,
    ReadAllDoneProjectsModel,
)
from src.core.schemas.done_project import CreateDoneProjectModel, UpdateDoneProjectModel


done_projects_router = APIRouter(prefix=settings.api.v1.done_projects_prefix)


@done_projects_router.post("", response_model=ReadDoneProjectModel)
async def create(
    project_repo: DoneProjectRepoDap, create_project: CreateDoneProjectModel,
):
    new = await project_repo.create(create_project)
    await project_repo.session.commit()
    return new


@done_projects_router.get("", response_model=ReadAllDoneProjectsModel)
async def get_all(
    project_repo: DoneProjectRepoDap,
    params: AllDoneProjectParamsDap,
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
    items = [ReadDoneProjectModel.model_validate(p) for p in projects]

    return ReadAllDoneProjectsModel(items=items, count=count)


@done_projects_router.get("/random", response_model=list[ReadDoneProjectModel])
async def get_random(project_repo: DoneProjectRepoDap, limit: int = Query(5)):
    return await project_repo.get_random(limit, public=True)


@done_projects_router.put("/{done_project_id}", response_model=ReadDoneProjectModel)
async def update(
    project_repo: DoneProjectRepoDap,
    done_project_id: UUID,
    update_model: UpdateDoneProjectModel,
    _: AdminDap,
):
    try:
        res = await project_repo.update(done_project_id, update_model)
        await project_repo.session.commit()
        return res
    except NoEntityByIdFound:
        raise HTTPException(404, "No done project found by id.")


@done_projects_router.delete("/{done_project_id}")
async def delete(
    project_repo: DoneProjectRepoDap,
    file_worker: FileWorkerServiceDap,
    done_project_id: UUID,
    _: AdminDap,
):
    try:
        await project_repo.remove(done_project_id)
        await project_repo.session.commit()

        project = await project_repo.get_by_id(done_project_id)
        image_files: list[str] = [image.url for image in project.images]
        await project_repo.remove(done_project_id)
        await project_repo.session.commit()

        for file in image_files:
            file_worker.remove(file)

        return {"success": True}
    except NoEntityByIdFound:
        raise HTTPException(404, "No done project found by id.")


@done_projects_router.get("/{done_project_id}", response_model=ReadDoneProjectModel)
async def get_by_id(project_repo: DoneProjectRepoDap, done_project_id: UUID):
    try:
        project = await project_repo.get_by_id(done_project_id)
        return project
    except NoEntityByIdFound:
        raise HTTPException(404, "No done project found by id.")
