from fastapi import APIRouter

from src.core.conifg import settings

from src.api.deps import AllParamsDap, DoneProjectRepoDap
from src.core.schemas import (
    ReadDoneProjectModel,
    ReadAllDoneProjectsModel,
)


done_projects_router = APIRouter(prefix=settings.api.v1.done_projects_prefix)


@done_projects_router.get("/", response_model=ReadAllDoneProjectsModel)
async def get_all_projects(project_repo: DoneProjectRepoDap, params: AllParamsDap):
    projects, count = await project_repo.get_all(
        params["offset"], params["limit"], params["sort_by"], params["is_desc"]
    )
    items = [ReadDoneProjectModel.model_validate(p) for p in projects]

    return ReadAllDoneProjectsModel(items=items, count=count)
