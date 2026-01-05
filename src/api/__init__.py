from fastapi import APIRouter

from src.api.v1 import api_v1_router
from src.core.conifg import settings


main_router = APIRouter(prefix=settings.api.api_prefix)
main_router.include_router(api_v1_router)
