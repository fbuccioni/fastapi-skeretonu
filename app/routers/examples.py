from fastapi import APIRouter, Depends, HTTPException
#from fastapi_contrib.serializers.common import ModelSerializer
from fastapi_jwt_auth import AuthJWT
#from fastapi_pagination import Page

from .. import models
#from ..util import mongodb
#from ..util.mongodb import get_or_404, partial_update, check_duplication, role_or_403
#from ..util.pydantic.partial_model import ObjectId

router = APIRouter(
    prefix="/example", tags=["Example"],
    responses={404: {"detail": "Not found"}},
)


"""
# Paged result for MongoDB
class InsurancePolicySerializer(ModelSerializer, models.Example):
    class Meta:
        model = models.db.InsurancePolicy


@router.get('/', tags=["Example"], response_model=Page[models.Example])
async def list_examples(auth: AuthJWT = Depends()) -> Page[models.Example]:
    auth.jwt_required()

    return await mongodb.paginator.contrib_paginate(
        serializer_class=ExampleSerializer,
    )
"""


@router.get('/{id}', tags=["Example"], response_model=models.Example)
async def retrieve_example(
    id: str, auth: AuthJWT = Depends()
) -> models.Example:
    auth.jwt_required()



@router.patch('/{id}', tags=["Example"], response_model=models.PartialExample)
#@mongodb.check_duplication(message="ID duplicated")
async def partial_update_example(
    id: str, example: models.PartialExample, auth: AuthJWT = Depends()
) -> models.PartialExample:
    auth.jwt_required()



@router.patch('/{id}', tags=["Example"], response_model=models.Example)
#@mongodb.check_duplication(message="ID duplicated")
async def create_example(
    id: str, example: models.Example, auth: AuthJWT = Depends()
) -> models.PartialExample:
    auth.jwt_required()
