from fastapi import APIRouter

from src.core.conifg import settings
from src.api.v1.projects import projects_router
from src.api.v1.done_projects import done_projects_router
from src.api.v1.images import images_router
from src.api.v1.files import files_router


api_v1_router = APIRouter(prefix=settings.api.v1.prefix)
api_v1_router.include_router(projects_router, tags=["Projects"])
api_v1_router.include_router(done_projects_router, tags=["Done Projects"])
api_v1_router.include_router(images_router, tags=["Images"])
api_v1_router.include_router(files_router, tags=["Files"])
