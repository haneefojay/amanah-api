from collections.abc import AsyncIterator

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.db.session import get_session
from app.main import create_app


async def test_health_reports_ok_with_a_working_database(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


async def test_health_returns_503_when_the_database_is_unreachable(settings: Settings) -> None:
    app = create_app(settings)

    class BrokenSession:
        async def execute(self, *_: object, **__: object) -> None:
            raise ConnectionError("database is down")

    async def broken() -> AsyncIterator[AsyncSession]:
        yield BrokenSession()  # type: ignore[misc]

    app.dependency_overrides[get_session] = broken
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as http:
        response = await http.get("/health")
    assert response.status_code == 503
    assert response.json() == {"status": "unavailable", "database": "unreachable"}


async def test_every_response_has_a_request_id(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert len(response.headers["x-request-id"]) >= 8


async def test_a_valid_incoming_request_id_is_kept(client: AsyncClient) -> None:
    response = await client.get("/health", headers={"X-Request-ID": "abc-12345678"})
    assert response.headers["x-request-id"] == "abc-12345678"


async def test_a_suspicious_incoming_request_id_is_replaced(client: AsyncClient) -> None:
    response = await client.get("/health", headers={"X-Request-ID": "bad id\twith spaces"})
    assert response.headers["x-request-id"] != "bad id\twith spaces"


async def test_unknown_routes_use_the_error_envelope(client: AsyncClient) -> None:
    response = await client.get("/api/nothing-here")
    assert response.status_code == 404
    assert response.json() == {"error": {"code": "NOT_FOUND", "message": "Not Found"}}


async def test_cors_allows_the_frontend_origin_with_credentials(client: AsyncClient) -> None:
    response = await client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert response.headers["access-control-allow-credentials"] == "true"


async def test_cors_does_not_allow_other_origins(client: AsyncClient) -> None:
    response = await client.get("/health", headers={"Origin": "https://evil.example"})
    assert "access-control-allow-origin" not in response.headers


async def test_openapi_document_is_served(client: AsyncClient) -> None:
    response = await client.get("/api/openapi.json")
    assert response.status_code == 200
    assert "/health" in response.json()["paths"]
