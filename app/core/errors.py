"""The standard error envelope: {"error": {"code": "SCREAMING_SNAKE", "message": "..."}}."""

from http import HTTPStatus

import structlog
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

log = structlog.get_logger()


def error_body(code: str, message: str) -> dict[str, dict[str, str]]:
    return {"error": {"code": code, "message": message}}


def _code_for(status: int) -> str:
    try:
        return HTTPStatus(status).name
    except ValueError:
        return "ERROR"


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_error(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            error_body(_code_for(exc.status_code), str(exc.detail)),
            status_code=exc.status_code,
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        first = exc.errors()[0] if exc.errors() else {}
        where = ".".join(str(part) for part in first.get("loc", ()))
        message = f"{where}: {first.get('msg', 'Invalid request')}" if where else "Invalid request"
        return JSONResponse(error_body("VALIDATION_ERROR", message), status_code=422)

    @app.exception_handler(Exception)
    async def unhandled_error(_: Request, exc: Exception) -> JSONResponse:
        # Never leak stack traces to clients (roadmap B12.1); log them instead.
        log.error("unhandled_exception", exc_info=exc)
        return JSONResponse(error_body("INTERNAL_ERROR", "Something went wrong."), status_code=500)
