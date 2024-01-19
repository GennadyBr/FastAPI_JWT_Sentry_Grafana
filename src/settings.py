"""File with settings and configs for the project"""
from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
)  # connect string for the real database


# REAL_DATABASE_URL = env.str(
#     "REAL_DATABASE_URL",
#     default="postgresql+asyncpg://postgres:postgres@db_pg_2401:5432/postgres",
# )  # connect string for the real database

APP_PORT = env.int("APP_PORT", default=8000)

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
SENTRY_URL: str = env.str(
    "SENTRY_URL",
    default="https://e94f707391cbbc8c1e27d0c3391c0564@o4505918059118592.ingest.sentry.io/4506592294797312",
)

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
