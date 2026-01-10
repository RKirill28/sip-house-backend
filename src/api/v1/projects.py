from uuid import UUID

from fastapi import APIRouter, UploadFile, Query, HTTPException

from src.core.conifg import settings
from src.core.schemas import CreateProjectModel, ReadProjectModel, UpdateProjectModel

from src.api.deps import FileSaverServiceDap, ValidatorServiceDap, ProjectRepoDap
from src.services.file_validator import GeneralValidationError


projects_router = APIRouter(prefix=settings.api.v1.projects_prefix)


@projects_router.post("/project", response_model=CreateProjectModel)
async def create_project(
    project_repo: ProjectRepoDap, create_project: CreateProjectModel
):
    new = await project_repo.create(create_project)
    return new


@projects_router.get("/", response_model=list[ReadProjectModel])
async def get_all_projects(project_repo: ProjectRepoDap):
    projects = await project_repo.get_all()
    return projects


@projects_router.post("/add_pdf_urls", response_model=ReadProjectModel)
async def add_pdf_urls(
    project_repo: ProjectRepoDap,
    update_model: UpdateProjectModel,
):
    project = await project_repo.update(update_model)
    await project_repo.session.commit()

    return project
