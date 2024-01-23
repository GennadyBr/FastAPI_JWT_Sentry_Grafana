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

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

from settings import settings
from api.v1.user_routers import user_router
from api.v1.db_routers import db_router
from api.v1.login_routers import login_router
from api.v1.service_routers import service_router
from api.v1.admin_routers import admin_router


# jaeger
def configure_tracer() -> None:
    """
    Трейсер - константный сэмплер, для трейсинга всех запросов.
    По умолчанию Jaeger сэмплирует только порядка 5%.
    """
    resource = Resource(attributes={SERVICE_NAME: "auth-service"})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.JEAGER_HOST,
                agent_port=settings.JEAGER_PORT_UDP,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )


if settings.enable_tracer:
    configure_tracer()  # Jaeger instrument for tracer, must be before app = FastAPI

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
    title="FastAPI_auth_2401",
)

# jaeger
FastAPIInstrumentor.instrument_app(
    app
)  # Jaeger instrument for tracer, must be after app = FastAPI

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
