import fastapi_contrib.db.client
import fastapi_contrib.db.utils
from fastapi_contrib.db.models import MongoDBModel, MongoDBTimeStampedModel
from pymongo.client_session import ClientSession
from pymongo.results import InsertOneResult

from ..mongodb import Empty
from ..pydantic.mongodb import ObjectId


async def insert(
    self,
    model: MongoDBModel,
    session: ClientSession = None,
    include=None,
    exclude=None,
) -> InsertOneResult:
    data = model.dict(include=include, exclude=exclude)
    data["_id"] = data.pop("id")
    if data["_id"] is Empty:
        data.pop("_id")
    collection_name = model.get_db_collection()
    collection = self.get_collection(collection_name)
    return await collection.insert_one(data, session=session)


def get_models(*klasses):
    if not klasses:
        klasses = (MongoDBModel, MongoDBTimeStampedModel)

    subclasses = []
    for klass in klasses:
        subclasses += [
            cls for cls in klass.__subclasses__()
            if cls != MongoDBTimeStampedModel
        ]

    for subclass in subclasses:
        subclasses += get_models(subclass)

    return subclasses


def emptify(*args):
    return Empty


fastapi_contrib.db.client.MongoDBClient.insert = insert
fastapi_contrib.db.utils.get_models = get_models
fastapi_contrib.db.utils.default_id_generator = emptify()
MongoDBModel.__annotations__['id'] = ObjectId
