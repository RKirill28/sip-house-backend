from uuid import UUID

from pydantic import Field

from src.core.enums import ObjectType
from src.core.schemas.base import MyBaseModel


class CreateMessageModel(MyBaseModel):
    user_name: str = Field(max_length=32, alias="userName")
    user_phone: str = Field(max_length=20, alias="userPhone")
    user_email: str = Field(max_length=100, alias="userEmail")
    object_type: ObjectType = Field(alias="objectType")
    comment: str = Field(max_length=255)


class MessageModel(MyBaseModel):
    user_name: str = Field(max_length=32, alias="userName")
    user_phone: str = Field(max_length=20)
    user_email: str = Field(max_length=100)
    object_type: ObjectType
    comment: str = Field(max_length=255)


class ReadMessageModel(CreateMessageModel):
    id: UUID
