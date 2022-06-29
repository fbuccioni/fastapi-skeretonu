from fastapi_contrib.db.models import MongoDBModel
import pymongo

from .. import example


class Example(example.Example, MongoDBModel):
    class Meta:
        include = ["id"]
        collection = "example"
        indexes = [
            pymongo.IndexModel(
                [("unique_value", 1), ("number", 1)], unique=True,
                name="unq_example_unique_value",
                collation={"locale": "simple", "strength": 2}
            )
        ]
