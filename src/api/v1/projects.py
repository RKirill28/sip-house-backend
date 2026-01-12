from fastapi import APIRouter, Query

from src.core.conifg import settings
from src.core.enums import ProjectSortBy
from src.core.schemas import CreateProjectModel, ReadProjectModel, UpdateProjectModel

from src.api.deps import ProjectRepoDap
from src.core.schemas import ReadAllProjectsModel


projects_router = APIRouter(prefix=settings.api.v1.projects_prefix)


@projects_router.post("/project", response_model=ReadProjectModel)
async def create_project(
    project_repo: ProjectRepoDap, create_project: CreateProjectModel
):
    new = await project_repo.create(create_project)
    await project_repo.session.commit()
    return new


@projects_router.get("/", response_model=ReadAllProjectsModel)
async def get_all_projects(
    project_repo: ProjectRepoDap,
    offset: int = Query(0),
    limit: int = Query(10),
    sort_by: ProjectSortBy = Query(),
    is_desk: bool = False,
):
    projects, count = await project_repo.get_all_with_count(
        offset, limit, sort_by, is_desk
    )
    items = [ReadProjectModel.model_validate(p) for p in projects]

    return ReadAllProjectsModel(items=items, count=count)


@projects_router.post("/add_pdf_urls", response_model=ReadProjectModel)
async def add_pdf_urls(
    project_repo: ProjectRepoDap,
    update_model: UpdateProjectModel,
):
    project = await project_repo.update(update_model)
    await project_repo.session.commit()

    return project


@projects_router.post("/random", response_model=list[ReadProjectModel])
async def get_random_project(project_repo: ProjectRepoDap, limit: int = Query(5)):
    return await project_repo.get_random(limit)
