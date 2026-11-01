"""GET /health: liveness plus a database check."""

import structlog
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

router = APIRouter(tags=["health"])
log = structlog.get_logger()


@router.get("/health")
async def health(session: AsyncSession = Depends(get_session)) -> JSONResponse:  # noqa: B008
    try:
        await session.execute(text("SELECT 1"))
    except Exception:
        log.warning("health_database_unreachable", exc_info=True)
        return JSONResponse({"status": "unavailable", "database": "unreachable"}, status_code=503)
    return JSONResponse({"status": "ok", "database": "ok"})
