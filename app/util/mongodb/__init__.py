from functools import wraps

from fastapi import HTTPException
from fastapi_contrib.db.models import MongoDBModel
from fastapi_contrib.serializers.common import ModelSerializer
from pymongo.errors import DuplicateKeyError

from . import paginator


class Empty(object):
    pass


async def get_or_404(model: MongoDBModel, **filter_kwargs):
    instance = await model.get(**filter_kwargs)

    if not instance:
        raise HTTPException(404)

    return instance


async def partial_update(serializer: ModelSerializer, **filter_kwargs):
    db_doc = await serializer.Meta.model.get(**filter_kwargs)

    if not db_doc:
        raise HTTPException(404)

    updated = await serializer.update_one(filter_kwargs=dict(**filter_kwargs))
    if updated.matched_count < 1:
        raise HTTPException(500, detail="Cannot perform update by unknown error")

    for prop, value in serializer.dict(skip_defaults=True).items():
        setattr(db_doc, prop, value)

    return db_doc


def check_duplication(message="ID already in use", field="id"):
    def _check_duplication(fn):
        nonlocal message, field

        @wraps(fn)
        async def _check_duplication_view(*args, **kwargs):
            nonlocal message, field

            try:
                return await fn(*args, **kwargs)
            except DuplicateKeyError:
                raise HTTPException(
                    400, {
                        "loc": ["body", field],
                        "msg": message,
                        "type": "value_error"
                    }
                )

        return _check_duplication_view

    return _check_duplication
