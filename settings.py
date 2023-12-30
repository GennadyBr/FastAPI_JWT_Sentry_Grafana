from envparse import Env


env_path = Env()

REAL_DATABASE_URL = env_path(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"
)
