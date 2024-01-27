from logging import getLogger
from random import randint

from fastapi import APIRouter

LOGGER = getLogger(__name__)
service_router = APIRouter()


@service_router.get("/ping")
async def ping():
    LOGGER.info("ping")
    a = randint(0, 10) % 2
    if a == 0:
        raise ValueError(f"{a=}")
    else:
        raise TypeError(f"{a=}")
    # return {"Success": True}


# verify Sentry via triggers an error
@service_router.get("/sentry-debug")
async def trigger_error():
    LOGGER.info("trigger_error")
    division_by_zero = 1 / 0
    return division_by_zero
