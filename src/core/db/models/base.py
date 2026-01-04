from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text, CHAR, VARCHAR

from uuid import UUID


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        VARCHAR(36), primary_key=True, server_default=text("(UUID())")
    )
