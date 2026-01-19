from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import VARCHAR


class Chat(Base):
    __tablename__ = "chats"

    username: Mapped[str | None] = mapped_column(VARCHAR(32), default=None)
    chat_id: Mapped[int]
