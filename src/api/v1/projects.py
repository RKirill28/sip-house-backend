from fastapi import APIRouter

from src.core.conifg import settings
from src.core.schemas.project import ProjectModel


projects_router = APIRouter(prefix=settings.api.v1.projects_prefix)


@projects_router.post("/project")
async def new_project(project: ProjectModel):
    return project
