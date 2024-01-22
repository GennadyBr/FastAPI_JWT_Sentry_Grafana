import os
import sys

sys.path.append(os.getcwd())
sys.path.append(os.path.dirname(os.getcwd()))
print(f"{sys.path}")

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import settings
from api.v1.user_routers import user_router
from api.v1.db_routers import db_router
from api.v1.login_routers import login_router
from api.v1.service_routers import service_router
from api.v1.admin_routers import admin_router

# sentry configuration
sentry_sdk.init(
    dsn=settings.SENTRY_URL,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# create instance of the app
app = FastAPI(
    debug=True,
    docs_url="/docs",
    title="FastAPI_auth_app4",
)
# Prometheus metrics
Instrumentator().instrument(app).expose(app)
# app.add_middleware(PrometheusMiddleware)
# app.add_route("/metrics", handle_metrics)

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(db_router, prefix="/db", tags=["db"])
main_api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
main_api_router.include_router(service_router, tags=["service"])
app.include_router(main_api_router)


@app.on_event("startup")
async def startup_event():
    """Initialize the redis cache"""
    redis = aioredis.from_url(
        url=settings.REDIS_URL, encoding="utf-8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
