from datetime import datetime
from uuid import UUID
from pydantic import Field
from .base import MyBaseModel


class CreateAdmin(MyBaseModel):
    username: str = Field(max_length=32)
    password: str = Field(max_length=64)


class UpdateAdminToken(MyBaseModel):
    id: UUID
    access_token: str
    expires_token: datetime | None = None


class CreateAdminResponse(MyBaseModel):
    id: UUID
    username: str


class LoginAdmin(CreateAdmin):
    pass


class LoginAdminResponse(CreateAdminResponse):
    pass


class Tokens(MyBaseModel):
    access: str
    refresh: str
