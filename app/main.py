"""Application factory and entry point (`uvicorn app.main:app`)."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.core.config import Settings, get_settings
from app.core.error_codes import CATALOGUE
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging
from app.core.request_id import RequestIdMiddleware
from app.db.session import create_engine, create_session_factory
from app.health import router as health_router
from app.modules import accountability, admin, audit, auth, campaigns, donations, organisations

# Every module is wired here and nowhere else; modules never import each other's internals.
MODULES = (auth, organisations, campaigns, donations, accountability, audit, admin)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.log_level, json_logs=settings.app_env in {"staging", "production"})

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_engine(settings.database_url)
        app.state.engine = engine
        app.state.session_factory = create_session_factory(engine)
        structlog.get_logger().info("startup", env=settings.app_env)
        try:
            yield
        finally:
            await engine.dispose()

    app = FastAPI(
        title="Amanah API",
        version="0.1.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url=None,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "X-Request-ID", "X-CSRF-Token"],
        expose_headers=["X-Request-ID"],
    )
    # Added last, so it is the outermost layer and the request ID reaches everything else.
    app.add_middleware(RequestIdMiddleware)
    register_error_handlers(app)
    app.include_router(health_router)
    for module in MODULES:
        for router in module.routers:
            app.include_router(router)
    app.openapi = lambda: build_openapi(app)  # type: ignore[method-assign]
    return app


def build_openapi(app: FastAPI) -> dict[str, Any]:
    """The contract: FastAPI's schema plus the error-code catalogue (`info.x-error-codes`)."""
    if app.openapi_schema is None:
        schema = get_openapi(
            title=app.title,
            version=app.version,
            description="Amanah API contract. Money is integer kobo; timestamps are UTC ISO 8601.",
            routes=app.routes,
        )
        schema["info"]["x-error-codes"] = {
            code: {"status": item.status, "meaning": item.meaning}
            for code, item in sorted(CATALOGUE.items())
        }
        app.openapi_schema = schema
    return app.openapi_schema


def __getattr__(name: str) -> FastAPI:
    # `app` is created lazily so importing this module never needs the environment,
    # but `uvicorn app.main:app` still fails fast at startup when it is incomplete.
    if name == "app":
        instance = create_app()
        globals()["app"] = instance
        return instance
    raise AttributeError(name)
