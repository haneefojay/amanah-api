"""Session-cookie security scheme shared by every protected router (ADR-011)."""

from fastapi import Security
from fastapi.security import APIKeyCookie

# Declared so OpenAPI lists the cookie scheme and every protected route references it.
session_cookie = APIKeyCookie(
    name="amanah_session",
    scheme_name="sessionCookie",
    auto_error=False,
    description="Server-side session in an httpOnly cookie (ADR-011). Sign in with "
    "POST /api/auth/login.",
)
requires_session = [Security(session_cookie)]
