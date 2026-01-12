from enum import Enum

from src.core.db.models.project import Project


class ObjectType(Enum):
    residential_house = "Дом для постоянного проживания"
    country_house = "Дачный дом"
    guest_house = "Гостевой дом"
    commersial_object = "Коммерческий объект"


class ProjectSortBy(Enum):
    NAME = ("name", Project.name)
    DESCRIPTION = ("description", Project.description)
    PRICE = ("price", Project.price)
    PRICE_DESCRIPTION = ("price_description", Project.price_description)

    @property
    def project_attr(self):
        return super().value[-1]

    @property
    def value(self):
        return super().value[0]
