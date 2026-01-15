from fastapi import APIRouter

from src.core.conifg import settings

from src.api.deps import DoneProjectRepoDap, AllDoneProjectParamsDap
from src.core.schemas import (
    ReadDoneProjectModel,
    ReadAllDoneProjectsModel,
)
from src.core.schemas.done_project import CreateDoneProjectModel


done_projects_router = APIRouter(prefix=settings.api.v1.done_projects_prefix)


@done_projects_router.post("", response_model=ReadDoneProjectModel)
async def create_project(
    project_repo: DoneProjectRepoDap, create_project: CreateDoneProjectModel
):
    new = await project_repo.create(create_project)
    await project_repo.session.commit()
    return new


@done_projects_router.get("", response_model=ReadAllDoneProjectsModel)
async def get_all_projects(
    project_repo: DoneProjectRepoDap, params: AllDoneProjectParamsDap
):
    projects, count = await project_repo.get_all(
        params["offset"], params["limit"], params["sort_by"], params["is_desc"]
    )
    items = [ReadDoneProjectModel.model_validate(p) for p in projects]

    return ReadAllDoneProjectsModel(items=items, count=count)
