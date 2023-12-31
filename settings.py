from envparse import Env


env_path = Env()

REAL_DATABASE_URL = env_path(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"
)

TEST_DATABASE_URL = env_path(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test"
)

TABLES_4_CLEANING = ["users"]
