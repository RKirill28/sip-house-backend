from uuid import UUID

from src.infra.db.repositories.admin import AdminRepository
from src.services.hasher import Hasher


class InvalidCredentials(Exception):
    """Неправильные реквизиты для входа"""


class UsernameIsAlreadyTaken(Exception):
    """Такой username уже занят"""


class RefreshTokenHasExpired(Exception):
    """Refresh токен истек"""


class NoRefreshToken(Exception):
    """Автор не имеет Refresh токена"""


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
