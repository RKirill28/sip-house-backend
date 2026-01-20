from uuid import UUID
from .base import MyBaseModel

from pydantic import Field


class CreateChatModel(MyBaseModel):
    chat_id: int
    username: str | None = Field(None, max_length=32)


class ChatModel(CreateChatModel):
    pass


class ReadChatModel(CreateChatModel):
    id: UUID
