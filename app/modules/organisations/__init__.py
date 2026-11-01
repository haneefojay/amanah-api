"""Organisations and verification documents. Public interface of the organisations module."""

from fastapi import APIRouter

from app.modules.organisations.router import public_router
from app.modules.organisations.schemas import OrganisationSummary, VerificationStatus

routers: tuple[APIRouter, ...] = (public_router,)

__all__ = ["OrganisationSummary", "VerificationStatus", "routers"]
