import os
import asyncpg
import asyncio
from typing import Generator, Any, Dict
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

import settings
from main import app
from db.session import get_db


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for tests to prevent async errors
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    """Run migrations for test DB"""
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade head")


@pytest.fixture(scope="session")
async def async_session_test():
    """Get test async session for test DB"""
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before each test."""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in settings.TABLES_4_CLEANING:
                await session.execute(f"""TRUNCATE TABLE {table_for_cleaning};""")


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the db session fixture to override
    the get_db dependence that is injected into routes
    """

    async def _get_test_db():
        """Get test async session for dependency_overrides of test DB"""
        try:
            test_engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
            test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
            yield test_async_session()
        finally:
            pass

    app.dependency_overrides[get_db]: Dict = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    """Create pool test getting user in DB via asyncpg connections"""
    pool = await asyncpg.create_pool("".join(settings.TEST_DATABASE_URL.split("+asyncpg")))
    yield pool
    pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    """Get user from database using asyncpg connection"""

    async def get_user_from_database_by_uuid(user_id: str):
        """Get user from database using asyncpg connection by user_id"""
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("""SELECT * FROM users WHERE user_id = $1""", user_id)

    return get_user_from_database_by_uuid
