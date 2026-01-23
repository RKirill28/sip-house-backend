from .base import Base

from datetime import datetime
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Admin(Base):
    __tablename__ = "admins"

    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(32))
    refresh_token: Mapped[UUID | None] = mapped_column(unique=True, default=None)
    expires_token: Mapped[datetime | None] = mapped_column(default=None)
