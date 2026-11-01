"""The OpenAPI document is the contract (B0.3). These tests keep it honest."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from httpx import AsyncClient

from app.core.config import Settings
from app.core.error_codes import CATALOGUE
from app.main import create_app

ROOT = Path(__file__).resolve().parents[2]
METHODS = {"get", "post", "put", "patch", "delete"}


@pytest.fixture(scope="module")
def schema() -> dict[str, Any]:
    app = create_app(Settings(database_url="postgresql+asyncpg://unused@localhost/unused"))
    return app.openapi()


def operations(schema: dict[str, Any]) -> list[tuple[str, str, dict[str, Any]]]:
    return [
        (method, path, op)
        for path, item in schema["paths"].items()
        for method, op in item.items()
        if method in METHODS
    ]


def test_committed_openapi_json_is_up_to_date() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "export_openapi.py"), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout


def test_is_openapi_3_with_an_error_catalogue(schema: dict[str, Any]) -> None:
    assert schema["openapi"].startswith("3.")
    assert set(schema["info"]["x-error-codes"]) == set(CATALOGUE)


def test_operation_ids_are_unique_and_every_route_is_tied_to_the_roadmap(
    schema: dict[str, Any],
) -> None:
    ids = [op["operationId"] for _, path, op in operations(schema) if path != "/health"]
    assert len(ids) == len(set(ids))
    for method, path, op in operations(schema):
        if path == "/health":
            continue
        assert op.get("x-roadmap", "").startswith("B"), f"{method} {path} has no x-roadmap"


@pytest.mark.parametrize("prefix", ["/api/org/", "/api/witness/", "/api/admin/"])
def test_role_routes_declare_the_session_cookie(schema: dict[str, Any], prefix: str) -> None:
    ops = [(m, p, o) for m, p, o in operations(schema) if p.startswith(prefix)]
    assert ops
    for method, path, op in ops:
        assert {"sessionCookie": []} in op.get("security", []), f"{method} {path}"
        codes = set(op["responses"])
        assert {"401", "403"} <= codes, f"{method} {path} must document 401 and 403"


def test_public_routes_need_no_session(schema: dict[str, Any]) -> None:
    for path in ("/api/campaigns", "/api/campaigns/{slug}", "/api/donations/{reference}"):
        assert "security" not in schema["paths"][path]["get"]


def test_error_responses_use_the_envelope(schema: dict[str, Any]) -> None:
    for method, path, op in operations(schema):
        for code, response in op["responses"].items():
            if code.startswith(("4", "5")) and code != "422":
                ref = response["content"]["application/json"]["schema"]["$ref"]
                assert ref.endswith("/ApiError"), f"{method} {path} {code}"


def test_money_fields_are_integers(schema: dict[str, Any]) -> None:
    for name, model in schema["components"]["schemas"].items():
        for field, prop in model.get("properties", {}).items():
            if field.lower().endswith("amount"):
                assert prop.get("type") == "integer", f"{name}.{field} must be integer kobo"


def test_donation_status_never_exposes_donor_contact(schema: dict[str, Any]) -> None:
    props = set(schema["components"]["schemas"]["DonationStatus"]["properties"])
    assert not {"donorEmail", "donorPhone", "email", "phone"} & props


async def test_stubs_answer_501_in_the_error_envelope(client: AsyncClient) -> None:
    response = await client.get("/api/campaigns")
    assert response.status_code == 501
    assert response.json()["error"]["code"] == "NOT_IMPLEMENTED"
    assert "B5.1" in response.json()["error"]["message"]


async def test_openapi_json_is_served(client: AsyncClient) -> None:
    response = await client.get("/api/openapi.json")
    assert response.status_code == 200
    assert json.loads(response.text)["info"]["title"] == "Amanah API"
