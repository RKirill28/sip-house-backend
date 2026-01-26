from enum import Enum

from src.core.db.models import Project, DoneProject, Message, Image


class ObjectType(Enum):
    residential_house = "Дом для постоянного проживания"
    country_house = "Дачный дом"
    guest_house = "Гостевой дом"
    commersial_object = "Коммерческий объект"


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
    pass
    # CREATED_AT = ("created_at", Message.created_at)
    # USERNAME = ("username", Message.username)
    # USER_PHONE = ("user_phone", Message.user_phone)
    # USER_EMAIL = ("user_email", Message.user_email)
    # COMMENT = ("comment", Message.comment)


class AdmibSortBy(SortBy):
    pass
