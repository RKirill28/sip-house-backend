from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.repositories import ProjectRepository, ImageRepository
from src.core.db.helper import get_session
from src.services.file_validator import GeneralValidatorService
from src.services.saver import FileSaverService


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_project_repo(session: SessionDep) -> ProjectRepository:
    return ProjectRepository(session)


def get_image_repo(session: SessionDep) -> ImageRepository:
    return ImageRepository(session)


def get_file_validator() -> GeneralValidatorService:
    return GeneralValidatorService()


def get_file_saver() -> FileSaverService:
    return FileSaverService()


ProjectRepoDap = Annotated[ProjectRepository, Depends(get_project_repo)]
ImageRepoDap = Annotated[ImageRepository, Depends(get_image_repo)]

ValidatorServiceDap = Annotated[GeneralValidatorService, Depends(get_file_validator)]
FileSaverServiceDap = Annotated[FileSaverService, Depends(get_file_saver)]
