from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text
from sqlalchemy.dialects.mysql import BINARY


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        BINARY(16),
        primary_key=True,
        server_default=text("(UUID_TO_BIN(UUID()))"),
    )
