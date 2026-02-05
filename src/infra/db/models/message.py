from .base import Base

from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import VARCHAR


from src.core.enums import ObjectType


class Message(Base):
    __tablename__ = "messages"

    created_at: Mapped[datetime] = mapped_column(
        # default=lambda: datetime.timestamp(),
        server_default=sqlalchemy.func.now(),
        server_onupdate=sqlalchemy.func.now(),
    )
    user_name: Mapped[str] = mapped_column(VARCHAR(32))
    user_phone: Mapped[str] = mapped_column(VARCHAR(20))
    user_email: Mapped[str | None] = mapped_column(VARCHAR(100), default=None)
    object_type: Mapped[ObjectType]
    comment: Mapped[str] = mapped_column(VARCHAR(255))
