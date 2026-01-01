from fastapi import APIRouter

from core.conifg import settings
from api.v1.projects import projects_router
from api.v1.images import images_router


api_v1_router = APIRouter(prefix=settings.api.v1.prefix)
api_v1_router.include_router(projects_router)
api_v1_router.include_router(iamges_router)
