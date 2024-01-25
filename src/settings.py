"""File with settings and configs for the project"""
import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Settings for FastAPI application"""

    # FastAPI
    APP_PORT = os.environ.get("APP_PORT", default=8000)
    PREFIX = "/app_2401"

    # token
    SECRET_KEY: str = os.environ.get("SECRET_KEY", default="secret_key")
    ALGORITHM: str = os.environ.get("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get(
        "ACCESS_TOKEN_EXPIRE_MINUTES", default=30
    )

    # sentry
    SENTRY_URL: str = os.environ.get(
        "SENTRY_URL",
        default="https://e94f707391cbbc8c1e27d0c3391c0564@o4505918059118592.ingest.sentry.io/4506592294797312",
    )

    # redis
    REDIS_URL: str = os.environ.get("REDIS_URL", default="redis://redis_2401:6379")
    # REDIS_URL: str = os.environ.get("REDIS_URL", default="redis://0.0.0.0:6379")
    REDIS_EXPIRE_SEC = 600

    # celery for GOOGLE GMAIL
    SMTP_USER = os.environ.get("SMTP_USER", default="")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", default="")
    SMTP_HOST = os.environ.get("SMTP_HOST", default="")
    SMTP_PORT = os.environ.get("SMTP_PORT", default=465)

    # router DB - Generate fake users
    QTY_FAKE_USERS = 10

    # PostgreSQL
    PG_USER = os.environ.get("PG_USER", default="postgres")
    PG_PWS = os.environ.get("PG_PWS", default="postgres")
    PG_HOST = os.environ.get("PG_HOST", default="db_pg_2401")  # localhost
    PG_PORT = os.environ.get("PG_PORT", default=5432)
    PG_DB = os.environ.get("PG_DB", default="postgres")
    # connect string for the real database
    REAL_DATABASE_URL = (
        f"postgresql+asyncpg://{PG_USER}:{PG_PWS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    )

    # PostgreSQL test
    PG_USER_TEST = os.environ.get("PG_USER_TEST", default="postgres_test")
    PG_PWS_TEST = os.environ.get("PG_PWS_TEST", default="postgres_test")
    PG_HOST_TEST = os.environ.get(
        "PG_HOST_TEST", default="localhost"
    )  # test_db_pg_2401
    PG_PORT_TEST = os.environ.get("PG_PORT_TEST", default=5433)
    PG_DB_TEST = os.environ.get("PG_DB_TEST", default="postgres_test")
    # connect string for the TEST database
    TEST_DATABASE_URL = f"postgresql+asyncpg://{PG_USER_TEST}:{PG_PWS_TEST}@{PG_HOST_TEST}:{PG_PORT_TEST}/{PG_DB_TEST}"

    # Jaeger
    enable_tracer = True
    JEAGER_HOST = os.environ.get("JEAGER_HOST", default="jaeger_2401")
    JEAGER_PORT_UDP = os.environ.get("JEAGER_PORT_UDP", default=6831)
    JEAGER_PORT_TCP = os.environ.get("JEAGER_PORT_TCP", default=16686)


settings = Settings()
