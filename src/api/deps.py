from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.repositories import (
    ProjectRepository,
    ImageRepository,
    DoneProjectRepository,
)
from src.core.db.helper import get_session
from src.core.enums import ProjectSortBy
from src.services.file_validator import GeneralValidatorService
from src.services.saver import FileSaverService


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_project_repo(session: SessionDep) -> ProjectRepository:
    return ProjectRepository(session)


def get_image_repo(session: SessionDep) -> ImageRepository:
    return ImageRepository(session)


def get_done_projects_repo(session: SessionDep) -> DoneProjectRepository:
    return DoneProjectRepository(session)


def get_file_validator() -> GeneralValidatorService:
    return GeneralValidatorService()


def get_file_saver() -> FileSaverService:
    return FileSaverService()


def get_all_params(
    offset: int = Query(0),
    limit: int = Query(10),
    sort_by: ProjectSortBy = Query(),
    is_desc: bool = False,
) -> dict:
    return {"offset": offset, "limit": limit, "sort_by": sort_by, "is_desc": is_desc}


ProjectRepoDap = Annotated[ProjectRepository, Depends(get_project_repo)]
ImageRepoDap = Annotated[ImageRepository, Depends(get_image_repo)]
DoneProjectRepoDap = Annotated[DoneProjectRepository, Depends(get_done_projects_repo)]

AllParamsDap = Annotated[dict, Depends(get_all_params)]

ValidatorServiceDap = Annotated[GeneralValidatorService, Depends(get_file_validator)]
FileSaverServiceDap = Annotated[FileSaverService, Depends(get_file_saver)]
