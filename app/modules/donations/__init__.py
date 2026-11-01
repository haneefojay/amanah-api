"""Donations, reservations, payments and excess. Public interface of the donations module."""

from fastapi import APIRouter

from app.modules.donations.router import public_router
from app.modules.donations.schemas import (
    ExcessListResponse,
    ExcessResolution,
    ExcessResolutionResponse,
)

routers: tuple[APIRouter, ...] = (public_router,)

__all__ = ["ExcessListResponse", "ExcessResolution", "ExcessResolutionResponse", "routers"]
