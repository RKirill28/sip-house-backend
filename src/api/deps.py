from typing import Annotated, Type, TypeVar
from uuid import UUID

from fastapi import Depends, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db.repositories import (
    ProjectRepository,
    ImageRepository,
    DoneProjectRepository,
    ChatRepository,
    MessageRepository,
    AdminRepository,
)
from src.infra.db.helper import get_session

from src.core.sort_by_enums import DoneProjectSortBy, ProjectSortBy, SortBy
from src.core.conifg import settings

from src.infra.tg import TelegramService
from src.services import FileWorkerService, ImageCompressor, GeneralValidatorService
from src.services.auth import AuthService
from src.services.token_service import JWTToken

import jwt

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


def get_mess_repo(session: SessionDep) -> MessageRepository:
    return MessageRepository(session)


def get_admin_repo(session: SessionDep) -> AdminRepository:
    return AdminRepository(session)


def get_file_validator() -> GeneralValidatorService:
    return GeneralValidatorService()


def get_file_worker() -> FileWorkerService:
    return FileWorkerService(ImageCompressor(settings.IMAGE_MAX_WIDTH))


def get_chat_repo(session: SessionDep) -> ChatRepository:
    return ChatRepository(session)


ProjectRepoDap = Annotated[ProjectRepository, Depends(get_project_repo)]
ImageRepoDap = Annotated[ImageRepository, Depends(get_image_repo)]
DoneProjectRepoDap = Annotated[DoneProjectRepository, Depends(get_done_projects_repo)]
MessageRepoDap = Annotated[MessageRepository, Depends(get_mess_repo)]
ChatRepoDap = Annotated[ChatRepository, Depends(get_chat_repo)]
AdminRepoDap = Annotated[AdminRepository, Depends(get_admin_repo)]


AllProjectParamsDap = Annotated[dict, Depends(get_params(ProjectSortBy))]
AllDoneProjectParamsDap = Annotated[dict, Depends(get_params(DoneProjectSortBy))]


ValidatorServiceDap = Annotated[GeneralValidatorService, Depends(get_file_validator)]
FileWorkerServiceDap = Annotated[FileWorkerService, Depends(get_file_worker)]


def get_tg_service(chat_repo: ChatRepoDap) -> TelegramService:
    return TelegramService(chat_repo)


TelegramServiceDap = Annotated[TelegramService, Depends(get_tg_service)]


def get_auth_service(admin_repo: AdminRepoDap) -> AuthService:
    return AuthService(admin_repo)


AuthServiceDap = Annotated[AuthService, Depends(get_auth_service)]


class TokenExpiredError(Exception):
    """Время жизни токена истекло"""


def get_admin(
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> UUID:
    if authorization is None:
        raise HTTPException(401, "Unauthorized")

    authorization = authorization.strip().replace("Bearer ", "")

    try:
        verified = JWTToken.verify_token(authorization)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

    sub = verified.get("sub")
    if not sub:
        raise HTTPException(401, "No token")
    return UUID(sub)


def get_optional_admin(
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> bool:
    if authorization is None:
        return False

    get_admin(authorization)
    return True


AdminDap = Annotated[UUID, Depends(get_admin)]
OptionalAdminDap = Annotated[bool, Depends(get_optional_admin)]
