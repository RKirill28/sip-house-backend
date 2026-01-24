from datetime import timezone, datetime
from uuid import UUID

from src.core.db.repositories.admin import AdminRepository
from src.services.hasher import Hasher
from src.core.schemas import CreateAdmin

from sqlalchemy.exc import IntegrityError


class InvalidCredentials(Exception):
    """Неправильные реквизиты для входа"""


class UsernameIsAlreadyTaken(Exception):
    """Такой username уже занят"""


class RefreshTokenHasExpired(Exception):
    """Refresh токен истек"""


class NoRefreshToken(Exception):
    """Автор не имеет Refresh токена"""


UserId = int


class AuthService:
    def __init__(self, admin_repo: AdminRepository) -> None:
        self.admin_repo = admin_repo

    async def authenticate(self, username: str, password: str) -> UUID:
        admin = await self.admin_repo.get_by_username(username)
        if not admin:
            raise InvalidCredentials

        check_password = Hasher.verify_password(password, admin.password)
        if not check_password:
            raise InvalidCredentials
        return admin.id

    # async def register(self, username: str, password: str) -> UUID:
    #     password = Hasher.hash_password(password)
    #
    #     try:
    #         new = await self.admin_repo.create(
    #             CreateAdmin(username=username, password=password)
    #         )
    #     except IntegrityError:
    #         raise UsernameIsAlreadyTaken
    #
    #     return new.id
    #
    # async def refresh_tokens(self, cookie_refresh_token: UUID) -> UUID:
    #     admin = await self.admin_repo.get_by_refresh_token(cookie_refresh_token)
    #     if not admin.expires_token:
    #         raise NoRefreshToken
    #     else:
    #         token_expires = admin.expires_token.replace(tzinfo=timezone.utc)
    #         if token_expires <= datetime.now(tz=timezone.utc):
    #             raise RefreshTokenHasExpired
    #         return admin.id
