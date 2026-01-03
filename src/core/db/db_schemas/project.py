from pydantic import BaseModel, FileUrl, Field

from src.core.db.db_schemas import DbImageModel


class DbProjectModel(BaseModel):
    name: str = Field(max_length=32)
    desctiption: str = Field(max_length=500)
    price: int
    price_description: str = Field(max_length=255)
    pdf_file: FileUrl
    images: list[DbImageModel]
