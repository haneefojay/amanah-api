"""Proves the test harness: a real PostgreSQL, and rollback isolation between tests."""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def test_session_talks_to_a_real_postgresql(db_session: AsyncSession) -> None:
    version = (await db_session.execute(text("SHOW server_version"))).scalar_one()
    assert version


async def test_writes_are_visible_inside_the_test_even_after_commit(
    db_session: AsyncSession,
) -> None:
    await db_session.execute(text("CREATE TABLE harness_probe (id integer)"))
    await db_session.execute(text("INSERT INTO harness_probe VALUES (1)"))
    await db_session.commit()
    count = (await db_session.execute(text("SELECT count(*) FROM harness_probe"))).scalar_one()
    assert count == 1


async def test_the_previous_test_left_nothing_behind(db_session: AsyncSession) -> None:
    exists = (
        await db_session.execute(text("SELECT to_regclass('public.harness_probe') IS NOT NULL"))
    ).scalar_one()
    assert exists is False
