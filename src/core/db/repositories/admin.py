from uuid import UUID
from sqlalchemy import select

from src.core.db.models import Admin
from src.core.db.repositories.base import NoEntityByIdFound
from src.core.enums import AdmibSortBy
from src.core.schemas import CreateAdmin, UpdateAdminToken
from src.core.db.repositories import BaseRepository


class AdminRepository(BaseRepository[Admin, CreateAdmin, AdmibSortBy]):
    model = Admin

    async def get_by_username(self, username: str) -> Admin | None:
        stmt = select(self.model).where(self.model.username == username)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_access_token(self, access_token: str) -> Admin:
        stmt = select(self.model).where(self.model.access_token == access_token)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def update_access_token(self, update_model: UpdateAdminToken) -> Admin:
        admin = await self.session.get(self.model, update_model.id)
        if admin is None:
            raise NoEntityByIdFound(f"Link with {update_model.id} id dont exists.")

        admin.access_token = update_model.access_token
        if update_model.expires_token:
            admin.expires_token = update_model.expires_token

        return admin
