from fastapi import APIRouter, Query

from src.core.conifg import settings

from src.api.deps import DoneProjectRepoDap, AllDoneProjectParamsDap, OptionalAdminDap
from src.core.schemas import (
    ReadDoneProjectModel,
    ReadAllDoneProjectsModel,
)
from src.core.schemas.done_project import CreateDoneProjectModel


done_projects_router = APIRouter(prefix=settings.api.v1.done_projects_prefix)


@done_projects_router.post("", response_model=ReadDoneProjectModel)
async def create(
    project_repo: DoneProjectRepoDap, create_project: CreateDoneProjectModel
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
