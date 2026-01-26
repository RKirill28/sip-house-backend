import jwt
import uuid

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, TypedDict

from src.core.conifg import settings


@dataclass(frozen=True)
class AccessToken:
    token: str
    expires: datetime
    max_age: int


@dataclass(frozen=True)
class RefreshToken:
    token: uuid.UUID
    expires: datetime
    max_age: int


class TokenPayload(TypedDict):
    sub: uuid.UUID
    exp: datetime


@dataclass(frozen=True)
class AccessTokenPayload:
    admin_id: uuid.UUID
    username: str


class JWTToken:
    @classmethod
    def get_tokens(cls, sub: uuid.UUID) -> AccessToken:
        expires = cls.get_max_age_date(settings.ACCESS_TOKEN_MAX_AGE_IN_MINUTES)
        data = {"sub": str(sub), "exp": expires}

        access_token = AccessToken(
            token=jwt.encode(data, settings.token_secret, algorithm="HS256"),
            max_age=settings.ACCESS_TOKEN_MAX_AGE_IN_MINUTES * 60,
            expires=expires,
        )

        return access_token

    @classmethod
    def get_max_age_date(cls, minutes: int) -> datetime:
        return datetime.now(timezone.utc) + timedelta(minutes=minutes)

    @staticmethod
    def verify_token(token: str) -> dict[str, Any]:
        return jwt.decode(token, settings.token_secret, ["HS256"])
