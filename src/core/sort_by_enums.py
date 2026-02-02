from enum import Enum

from src.infra.db.models.done_project import DoneProject
from src.infra.db.models.image import Image
from src.infra.db.models.project import Project
from src.infra.db.models.message import Message
from src.infra.db.models.chat import Chat


class SortBy(Enum):
    @property
    def project_attr(self):
        return super().value[-1]

    @property
    def value(self):
        return super().value[0]


class ProjectSortBy(SortBy):
    NAME = ("name", Project.name)
    DESCRIPTION = ("description", Project.description)
    PRICE = ("price", Project.price)
    PRICE_DESCRIPTION = ("price_description", Project.price_description)


class ImageSortBy(SortBy):
    NAME = ("name", Image.name)
    DESCRIPTION = ("description", Image.description)


class DoneProjectSortBy(SortBy):
    NAME = ("name", DoneProject.name)
    ADDRESS = ("address", DoneProject.address)


class MessageSortBy(SortBy):
    CREATED_AT = ("created_at", Message.created_at)
    USER_PHONE = ("user_phone", Message.user_phone)
    USER_EMAIL = ("user_email", Message.user_email)
    COMMENT = ("comment", Message.comment)


class ChatSortBy(SortBy):
    USERNAME = ("username", Chat.username)
    CHAT_ID = ("chat_id", Chat.chat_id)


class AdminSortBy(SortBy):
    pass
