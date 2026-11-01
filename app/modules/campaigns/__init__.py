"""Campaigns, items and the lifecycle. Public interface of the campaigns module."""

from fastapi import APIRouter

from app.modules.campaigns.router import org_router, public_router
from app.modules.campaigns.schemas import (
    CampaignDetailResponse,
    CampaignListResponse,
    CampaignStatus,
    OrganisationProfileResponse,
    OrgCampaignResponse,
)

routers: tuple[APIRouter, ...] = (
    public_router,
    org_router,
)

__all__ = [
    "CampaignDetailResponse",
    "CampaignListResponse",
    "CampaignStatus",
    "OrgCampaignResponse",
    "OrganisationProfileResponse",
    "routers",
]
