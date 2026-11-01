"""Platform admin back office. Public interface of the admin module."""

from fastapi import APIRouter

from app.modules.admin.router import admin_router

routers: tuple[APIRouter, ...] = (admin_router,)

__all__ = ["routers"]
