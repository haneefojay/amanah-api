"""Helpers shared by the routers: documented error responses and not-yet-built stubs."""

from typing import Any, NoReturn

from fastapi import Security
from fastapi.security import APIKeyCookie

from app.schemas.common import ApiError

# Declared so OpenAPI lists the cookie scheme and every protected route references it.
session_cookie = APIKeyCookie(
    name="amanah_session",
    scheme_name="sessionCookie",
    auto_error=False,
    description="Server-side session in an httpOnly cookie (ADR-011). Sign in with "
    "POST /api/auth/login.",
)
requires_session = [Security(session_cookie)]


class NotImplementedYet(Exception):
    """Raised by contract stubs. Becomes a 501 NOT_IMPLEMENTED error envelope."""

    def __init__(self, roadmap_id: str) -> None:
        super().__init__(f"Not built yet ({roadmap_id}).")
        self.roadmap_id = roadmap_id


def stub(roadmap_id: str) -> NoReturn:
    raise NotImplementedYet(roadmap_id)


def roadmap(roadmap_id: str) -> dict[str, Any]:
    """OpenAPI extensions tying an operation to its roadmap item. Flip `x-implemented` when done."""
    return {"x-roadmap": roadmap_id, "x-implemented": False}


def errors(*codes: int) -> dict[int | str, dict[str, Any]]:
    descriptions = {
        400: "Bad request",
        401: "Not signed in",
        403: "Not allowed for this role or organisation",
        404: "Not found",
        409: "Conflicts with the current state (see error.code)",
        413: "File too large",
        415: "Unsupported file type",
        422: "Validation error",
        429: "Too many requests",
        501: "Not built yet",
    }
    return {code: {"model": ApiError, "description": descriptions[code]} for code in codes}
