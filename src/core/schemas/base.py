from pydantic import BaseModel


class MyBaseModel(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        # "validate_by_alias": True,
    }
