"""Sign in, sign out and the current user (B2). Contract stubs."""

from fastapi import APIRouter, Response

from app.core.security import requires_session
from app.core.stubs import errors, roadmap, stub
from app.modules.auth.schemas import CurrentUserResponse, LoginRequest

auth_router = APIRouter(prefix="/api", tags=["auth"])


@auth_router.post(
    "/auth/login",
    operation_id="login",
    summary="Sign in",
    description="Sets the httpOnly session cookie. Wrong credentials always answer the same "
    "generic 401 INVALID_CREDENTIALS. Rate limited.",
    response_model=CurrentUserResponse,
    responses=errors(401, 422, 429),
    openapi_extra=roadmap("B2.1"),
)
async def login(body: LoginRequest) -> None:
    stub("B2.1")


@auth_router.post(
    "/auth/logout",
    operation_id="logout",
    summary="Sign out",
    description="Ends the session and clears the cookie.",
    status_code=204,
    response_class=Response,
    responses=errors(401),
    dependencies=requires_session,
    openapi_extra=roadmap("B2.1"),
)
async def logout() -> None:
    stub("B2.1")


@auth_router.get(
    "/me",
    operation_id="getCurrentUser",
    summary="The signed-in user",
    description="Role and organisation memberships. Donors are guests and have no account.",
    response_model=CurrentUserResponse,
    responses=errors(401),
    dependencies=requires_session,
    openapi_extra=roadmap("B2.3"),
)
async def get_current_user() -> None:
    stub("B2.3")
