from .base import Base

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import Mapped, mapped_column


class Admin(Base):
    __tablename__ = "admins"

    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(64))
    access_token: Mapped[str | None] = mapped_column(TEXT(1000), default=None)
    expires_token: Mapped[datetime | None] = mapped_column(default=None)
