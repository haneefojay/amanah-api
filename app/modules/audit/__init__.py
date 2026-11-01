"""The append-only audit log. Public interface of the audit module."""

from fastapi import APIRouter

from app.modules.audit.schemas import AuditLogResponse

routers: tuple[APIRouter, ...] = ()

__all__ = ["AuditLogResponse", "routers"]
