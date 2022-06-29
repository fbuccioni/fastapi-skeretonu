from fastapi import APIRouter

from . import auth
from . import examples

router = APIRouter(
    prefix="/api/v1",
    # dependencies=[Depends(get_token_header)],
    responses={404: {"detail": "Not found"}},
)

router.include_router(auth.router)
router.include_router(examples.router)
