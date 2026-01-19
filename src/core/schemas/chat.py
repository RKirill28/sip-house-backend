from uuid import UUID
from .base import MyBaseModel

from pydantic import Field


class CreateChatModel(MyBaseModel):
    username: str | None = Field(None, max_length=32)
    chat_id: int


class ReadChatModel(CreateChatModel):
    id: UUID
