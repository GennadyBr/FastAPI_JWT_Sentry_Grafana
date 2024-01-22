"""File with settings and configs for the project"""
from envparse import Env
from pydantic import BaseSettings

env = Env()


class Settings(BaseSettings):
    """Settings for FastAPI application"""

    # FastAPI port
    APP_PORT = env.int("APP_PORT", default=8000)

    # token
    SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
    ALGORITHM: str = env.str("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int(
        "ACCESS_TOKEN_EXPIRE_MINUTES", default=30
    )

    # sentry
    SENTRY_URL: str = env.str(
        "SENTRY_URL",
        default="https://e94f707391cbbc8c1e27d0c3391c0564@o4505918059118592.ingest.sentry.io/4506592294797312",
    )

    # redis
    # REDIS_URL: str = env.str("REDIS_URL", default="redis://redis_2401:6379")
    REDIS_URL: str = env.str("REDIS_URL", default="redis://0.0.0.0:6379")
    REDIS_EXPIRE_SEC = 600

    # celery for GOOGLE GMAIL
    SMTP_USER = env.str("SMTP_USER", default="")
    SMTP_PASSWORD = env.str("SMTP_PASSWORD", default="")
    SMTP_HOST = env.str("SMTP_HOST", default="")
    SMTP_PORT = env.int("SMTP_PORT", default=465)

    # router DB - Generate fake users
    QTY_FAKE_USERS = 10

    # REAL_DATABASE_URL = env.str(
    #     "REAL_DATABASE_URL",
    #     default="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
    # )  # connect string for the real database

    REAL_DATABASE_URL = env.str(
        "REAL_DATABASE_URL",
        default="postgresql+asyncpg://postgres:postgres@db_pg_2401:5432/postgres",
    )  # connect string for the real database

    # test envs
    TEST_DATABASE_URL = env.str(
        "TEST_DATABASE_URL",
        default="postgresql+asyncpg://postgres_test:postgres_test@localhost:5433/postgres_test",
    )  # connect string for the test database

    # # test envs docker
    # TEST_DATABASE_URL = env.str(
    #     "TEST_DATABASE_URL",
    #     default="postgresql+asyncpg://postgres_test:postgres_test@test_db_pg_2401:5432/postgres_test",
    # )  # connect string for the test database


settings = Settings()
