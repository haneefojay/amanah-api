"""Shared fixtures.

* Tests run against a real PostgreSQL (`TEST_DATABASE_URL`), never SQLite or mocks.
* The schema is built once per run by applying every migration to the test database.
* Each test gets a session inside a transaction that is rolled back afterwards, so tests
  cannot affect each other. Code under test may call `commit()`: it only releases a savepoint.
"""

import os
import subprocess
import sys
from collections.abc import AsyncIterator, Iterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import Settings
from app.db.session import get_session
from app.main import create_app

DEFAULT_TEST_DATABASE_URL = "postgresql+asyncpg://amanah@localhost:5432/amanah_test"
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", DEFAULT_TEST_DATABASE_URL)


def run_alembic(database_url: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Run the real Alembic CLI against `database_url` in a child process."""
    env = {**os.environ, "DATABASE_URL": database_url}
    return subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture(scope="session", autouse=True)
def migrated_database() -> Iterator[None]:
    result = run_alembic(TEST_DATABASE_URL, "upgrade", "head")
    assert result.returncode == 0, result.stderr
    yield


@pytest.fixture
def settings() -> Settings:
    return Settings(  # type: ignore[call-arg]
        _env_file=None,
        app_env="test",
        database_url=TEST_DATABASE_URL,
        cors_origins=["http://localhost:3000"],
    )


@pytest.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    """A session wrapped in an outer transaction that is always rolled back."""
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    async with engine.connect() as connection:
        outer = await connection.begin()
        factory = async_sessionmaker(
            bind=connection, expire_on_commit=False, join_transaction_mode="create_savepoint"
        )
        async with factory() as session:
            yield session
        await outer.rollback()
    await engine.dispose()


@pytest.fixture
async def client(settings: Settings, db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    """An HTTP client for the app, using the rolled-back test session."""
    app = create_app(settings)

    async def override_session() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_session] = override_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
        yield http
