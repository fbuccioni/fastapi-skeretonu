from typing import Optional, List
from pydantic import BaseModel, Field
from .abstract import AbstractSharedModel

from ..util.pydantic import partial_model
# from ..util.pydantic import ObjectId


class Example(AbstractSharedModel, BaseModel):
    # id: Optional[ObjectId] = Field(title="ID")
    example_property: int = Field(title="Example propert")
    optional_property: Optional[List["str"]] = Field(title="Example optional property")

    class Config:
        schema_extra = {
            "example": {
                "shared": "Value",
                "example_property": 1234
            }
        }


@partial_model
class PartialExample(Example):
    pass
