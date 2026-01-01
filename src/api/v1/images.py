from fastapi import APIRouter

from core.conifg import settings


images_router = APIRouter(prefix=settings.api.v1.images_prefix)
