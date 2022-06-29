import bson
import bson.errors
from pydantic.json import ENCODERS_BY_TYPE


class ObjectId(bson.ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        raise_error = False

        try:
            if isinstance(v, str):
                v = bson.ObjectId(v)

            if (
                not isinstance(v, (bson.ObjectId, cls))
                or not bson.ObjectId.is_valid(v)
            ):
                raise_error = True
        except bson.errors.InvalidId:
            raise_error = True

        if raise_error:
            raise ValueError("Invalid ObjectId")

        return v

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


if ObjectId not in ENCODERS_BY_TYPE:
    ENCODERS_BY_TYPE[ObjectId] = str
    ENCODERS_BY_TYPE[bson.ObjectId] = str
