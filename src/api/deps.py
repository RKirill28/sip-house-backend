from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.repositories import ProjectRepository, ImageRepository
from src.core.db.helper import get_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_project_repo(session: SessionDep) -> ProjectRepository:
    return ProjectRepository(session)


def get_image_repo(session: SessionDep) -> ImageRepository:
    return ImageRepository(session)


ProjectRepoDap = Annotated[ProjectRepository, Depends(get_project_repo)]
ImageRepoDap = Annotated[ImageRepository, Depends(get_image_repo)]
