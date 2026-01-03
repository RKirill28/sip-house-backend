from pydantic import BaseModel, FileUrl, Field


class DBImageModel(BaseModel):
    url: FileUrl
    name: str = Field(max_length=32)
    description: str = Field(max_length=255)
    main_image: bool
    sort: int
