"""Migrations apply to an empty database, roll back, and apply again (B0.4)."""

import uuid
from collections.abc import AsyncIterator

import asyncpg
import pytest

from tests.conftest import TEST_DATABASE_URL, run_alembic


def _admin_dsn() -> str:
    base = TEST_DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    return base.rsplit("/", 1)[0] + "/postgres"


@pytest.fixture
async def scratch_database_url() -> AsyncIterator[str]:
    name = f"amanah_migrations_{uuid.uuid4().hex[:8]}"
    admin = await asyncpg.connect(_admin_dsn())
    await admin.execute(f'CREATE DATABASE "{name}"')
    try:
        yield TEST_DATABASE_URL.rsplit("/", 1)[0] + f"/{name}"
    finally:
        await admin.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')
        await admin.close()


async def test_migrations_apply_roll_back_and_apply_again(scratch_database_url: str) -> None:
    for args in (("upgrade", "head"), ("downgrade", "base"), ("upgrade", "head")):
        result = run_alembic(scratch_database_url, *args)
        assert result.returncode == 0, f"alembic {' '.join(args)} failed: {result.stderr}"


async def test_there_is_a_single_head_revision(scratch_database_url: str) -> None:
    result = run_alembic(scratch_database_url, "heads")
    assert result.returncode == 0, result.stderr
    assert len(result.stdout.strip().splitlines()) == 1
