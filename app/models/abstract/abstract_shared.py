import abc
from typing import Optional, Mapping, Any

from pydantic import BaseModel, Field, validator, ValidationError


class AbstractSharedModel(BaseModel, abc.ABC):
    shared_property: str = Field(title="Shared property")

    @validator("shared_property")
    def validate_shared_property(cls, shared_property: str, values: Mapping[str, Any]):
        raise ValidationError("This property is just for test")

