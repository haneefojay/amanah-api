import os
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def make(**overrides: object) -> Settings:
    values: dict[str, object] = {"database_url": "postgresql+asyncpg://u:p@localhost/db"}
    values.update(overrides)
    return Settings(_env_file=None, **values)  # type: ignore[call-arg, arg-type]


def test_database_url_is_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ValidationError, match="database_url"):
        Settings(_env_file=None)  # type: ignore[call-arg]


def test_database_url_must_use_the_async_driver() -> None:
    with pytest.raises(ValidationError, match="postgresql\\+asyncpg"):
        make(database_url="postgresql://u:p@localhost/db")


def test_cors_origins_are_split_from_a_comma_separated_string() -> None:
    settings = make(cors_origins="http://localhost:3000, https://amanah.example")
    assert settings.cors_origins == ["http://localhost:3000", "https://amanah.example"]


def test_wildcard_cors_origin_is_rejected() -> None:
    with pytest.raises(ValidationError, match="explicit origins"):
        make(cors_origins="*")


def test_startup_fails_fast_when_a_required_variable_is_missing(tmp_path: Path) -> None:
    # Run from an empty directory so a developer's local .env cannot supply the value.
    env = {k: v for k, v in os.environ.items() if k != "DATABASE_URL"}
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2])
    result = subprocess.run(
        [sys.executable, "-c", "from app.main import create_app; create_app()"],
        env=env,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "database_url" in result.stderr.lower()
