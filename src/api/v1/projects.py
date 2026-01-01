from fastapi import APIRouter

from core.conifg import settings


projects_router = APIRouter(prefix=settings.api.v1.projects_prefix)
