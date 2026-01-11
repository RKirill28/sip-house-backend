from enum import Enum


class ObjectType(Enum):
    residential_house = "Дом для постоянного проживания"
    country_house = "Дачный дом"
    guest_house = "Гостевой дом"
    commersial_object = "Коммерческий объект"


class ProjectSortBy(Enum):
    NAME = "name"
    DESCRIPTION = "description"
    PRICE = "price"
    PRICE_DESCRIPTION = "price_description"
