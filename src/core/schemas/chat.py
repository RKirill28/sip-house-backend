from uuid import UUID
from .base import MyBaseModel

from pydantic import Field


class CreateChatModel(MyBaseModel):
    chat_id: int
    username: str | None = Field(None, max_length=32)
    model_config = {
        'frozen': True
    }


class ReadChatModel(CreateChatModel):
    id: UUID
