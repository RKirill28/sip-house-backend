from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import VARCHAR


class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str | None] = mapped_column(VARCHAR(32), default=None)
