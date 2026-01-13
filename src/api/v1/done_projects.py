from fastapi import APIRouter, Query

from src.core.conifg import settings
from src.core.enums import ProjectSortBy
from src.core.schemas import CreateProjectModel, ReadProjectModel, UpdateProjectModel

from src.api.deps import DoneProjectRepository
from src.core.schemas import (
    ReadDoneProjectModel,
    ReadAllDoneProjectsModel,
    CreateDoneProjectModel,
)


done_projects_router = APIRouter(prefix=settings.api.v1.done_projects_prefix)

# @done_projects_router.get("/", response_model=ReadAllProjectsModel)
# async def get_all_projects(
#     project_repo: ProjectRepoDap,
#     offset: int = Query(0),
#     limit: int = Query(10),
#     sort_by: ProjectSortBy = Query(),
#     is_desc: bool = False,
# ):
#     projects, count = await project_repo.get_all(offset, limit, sort_by, is_desc)
#     items = [ReadProjectModel.model_validate(p) for p in projects]
#
#     return ReadAllProjectsModel(items=items, count=count)
#
