from uuid import UUID
from fastapi import APIRouter, HTTPException, Query

from src.core.conifg import settings
from src.core.db.repositories.base import NoEntityByIdFound
from src.core.schemas import CreateProjectModel, ReadProjectModel, UpdateProjectModel

from src.api.deps import ProjectRepoDap, AllParamsDap
from src.core.schemas import ReadAllProjectsModel


projects_router = APIRouter(prefix=settings.api.v1.projects_prefix)


@projects_router.post("/project", response_model=ReadProjectModel)
async def create_project(
    project_repo: ProjectRepoDap, create_project: CreateProjectModel
):
    new = await project_repo.create(create_project)
    return new


@projects_router.get("/", response_model=ReadAllProjectsModel)
async def get_all_projects(
    project_repo: ProjectRepoDap,
    params: AllParamsDap,
):
    projects, count = await project_repo.get_all(
        params["offset"], params["limit"], params["sort_by"], params["is_desc"]
    )
    items = [ReadProjectModel.model_validate(p) for p in projects]

    return ReadAllProjectsModel(items=items, count=count)


@projects_router.get("/project/{project_id}", response_model=ReadProjectModel)
async def get_project_by_id(project_repo: ProjectRepoDap, project_id: UUID):
    try:
        project = await project_repo.get_by_id(project_id)
    except NoEntityByIdFound:
        raise HTTPException(404, "No project found by id.")

    return project


@projects_router.post("/add_pdf_urls", response_model=ReadProjectModel)
async def add_pdf_urls(
    project_repo: ProjectRepoDap,
    update_model: UpdateProjectModel,
):
    try:
        project = await project_repo.update(update_model)
    except NoEntityByIdFound:
        raise HTTPException(404, "No project found by id.")

    await project_repo.session.commit()

    return project


@projects_router.get("/random", response_model=list[ReadProjectModel])
async def get_random_project(project_repo: ProjectRepoDap, limit: int = Query(5)):
    return await project_repo.get_random(limit)
