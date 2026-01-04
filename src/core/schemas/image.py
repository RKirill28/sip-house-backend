from pydantic import BaseModel, Field, FileUrl


class ImageModel(BaseModel):
    url: FileUrl | None = None
    name: str = Field(max_length=32)
    description: str = Field(max_length=255)
    main_image: bool
    sort: int
