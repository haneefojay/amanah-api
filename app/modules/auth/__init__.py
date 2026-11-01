"""Sessions and users. Public interface of the auth module."""

from fastapi import APIRouter

from app.modules.auth.router import auth_router
from app.modules.auth.schemas import CurrentUserResponse

routers: tuple[APIRouter, ...] = (auth_router,)

__all__ = ["CurrentUserResponse", "routers"]
