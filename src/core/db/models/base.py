from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.mysql import BINARY


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        BINARY(16),
        primary_key=True,
        default=lambda: uuid4().bytes,
    )
