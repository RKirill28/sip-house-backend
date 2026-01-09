from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.db.enums import ObjectType


class CreateMessageModel(BaseModel):
    created_at: datetime
    username: str = Field(max_length=32)
    user_phone: str = Field(max_length=20)
    user_email: str = Field(max_length=100)
    object_type: ObjectType
    comment: str = Field(max_length=255)


class ReadMessageModel(CreateMessageModel):
    id: UUID
