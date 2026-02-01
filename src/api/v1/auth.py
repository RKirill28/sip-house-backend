import uuid

from fastapi import APIRouter, HTTPException

from src.services.token_service import AccessToken, JWTToken
from src.core.schemas import LoginAdmin, UpdateAdminToken
from src.core.db.repositories import AdminRepository
from src.core.conifg import settings
from src.api.deps import AdminDap, AdminRepoDap, AuthServiceDap

from src.services.auth import (
    InvalidCredentials,
)


auth_router = APIRouter(prefix=settings.api.v1.auth_prefix)

# TODO: service login.py and use login() func for reg and login


async def update_token(admin_id: uuid.UUID, admin_repo: AdminRepository) -> AccessToken:
    """
    Получает новый access токен и добавляет его в бд
    """
    token = JWTToken.get_tokens(admin_id)
    # WARN: access token save in db
    update_admin = UpdateAdminToken(
        id=admin_id, access_token=token.token, expires_token=token.expires
    )
    await admin_repo.update_access_token(update_admin)
    return token


@auth_router.post("/get_token")
async def get_token(
    login_scheme: LoginAdmin,
    admin_repo: AdminRepoDap,
    auth_service: AuthServiceDap,
):
    try:
        admin_id = await auth_service.authenticate(
            login_scheme.username, login_scheme.password
        )
    except InvalidCredentials:
        raise HTTPException(401, "Invalid username or password.")

    access_token = await update_token(admin_id, admin_repo)

    return {
        "success": True,
        "token": access_token.token,
        "expires": access_token.expires,
        "maxAge": access_token.max_age,
    }


@auth_router.get("/me")
async def me(admin: AdminDap):
    return {"success": True, "role": "admin", "id": admin}
