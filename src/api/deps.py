from typing import Annotated, Type, TypeVar

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.repositories import (
    ProjectRepository,
    ImageRepository,
    DoneProjectRepository,
)
from src.core.db.helper import get_session
from src.core.enums import DoneProjectSortBy, ProjectSortBy, SortBy
from src.core.conifg import settings
from src.services import FileWorkerService, ImageCompressor, GeneralValidatorService


SessionDep = Annotated[AsyncSession, Depends(get_session)]

T = TypeVar("T", bound=SortBy)


def get_params(sort_enum: Type[T]):
    def dep(
        offset: int = Query(0),
        limit: int = Query(10),
        sort_by: sort_enum = Query(),  # type: ignore
        is_desc: bool = Query(False),
    ) -> dict:
        return {
            "offset": offset,
            "limit": limit,
            "sort_by": sort_by,
            "is_desc": is_desc,
        }

    return dep


def get_project_repo(session: SessionDep) -> ProjectRepository:
    return ProjectRepository(session)


def get_image_repo(session: SessionDep) -> ImageRepository:
    return ImageRepository(session)


def get_done_projects_repo(session: SessionDep) -> DoneProjectRepository:
    return DoneProjectRepository(session)


def get_file_validator() -> GeneralValidatorService:
    return GeneralValidatorService()


def get_file_worker() -> FileWorkerService:
    return FileWorkerService(ImageCompressor(settings.IMAGE_MAX_WIDTH))


ProjectRepoDap = Annotated[ProjectRepository, Depends(get_project_repo)]
ImageRepoDap = Annotated[ImageRepository, Depends(get_image_repo)]
DoneProjectRepoDap = Annotated[DoneProjectRepository, Depends(get_done_projects_repo)]


AllProjectParamsDap = Annotated[dict, Depends(get_params(ProjectSortBy))]
AllDoneProjectParamsDap = Annotated[dict, Depends(get_params(DoneProjectSortBy))]


ValidatorServiceDap = Annotated[GeneralValidatorService, Depends(get_file_validator)]
FileWorkerServiceDap = Annotated[FileWorkerService, Depends(get_file_worker)]
