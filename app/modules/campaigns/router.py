"""Public campaign catalogue and the organisation campaign dashboard (B4, B5). Contract stubs."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.core.security import requires_session
from app.core.stubs import errors, roadmap, stub
from app.modules.campaigns.schemas import (
    CampaignCreate,
    CampaignDetailResponse,
    CampaignEdit,
    CampaignListResponse,
    OrganisationProfileResponse,
    OrgCampaignListResponse,
    OrgCampaignResponse,
)

public_router = APIRouter(prefix="/api", tags=["public"])

org_router = APIRouter(
    prefix="/api/org",
    tags=["organisation"],
    dependencies=requires_session,
    responses=errors(401, 403),
)


@public_router.get(
    "/campaigns",
    operation_id="listCampaigns",
    summary="List public campaigns",
    description="Live and recently completed campaigns, with the values the filters can offer.",
    response_model=CampaignListResponse,
    responses=errors(422),
    openapi_extra=roadmap("B5.1"),
)
async def list_campaigns(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(alias="pageSize", ge=1, le=50)] = 6,
    city: str | None = None,
    organisation_id: Annotated[UUID | None, Query(alias="organisationId")] = None,
) -> None:
    stub("B5.1")


@public_router.get(
    "/campaigns/{slug}",
    operation_id="getCampaign",
    summary="A campaign with its accountability data",
    description="Items, witness confirmations, expenses, evidence and updates in one response. "
    "Drafts and unknown slugs answer 404.",
    response_model=CampaignDetailResponse,
    responses=errors(404),
    openapi_extra=roadmap("B5.2"),
)
async def get_campaign(slug: str) -> None:
    stub("B5.2")


@public_router.get(
    "/organisations/{organisation_id}",
    operation_id="getOrganisation",
    summary="A verified organisation's public profile",
    description="Unverified organisations answer 404. Type and registration number are never "
    "public.",
    response_model=OrganisationProfileResponse,
    responses=errors(404),
    openapi_extra=roadmap("B3.4"),
)
async def get_organisation(organisation_id: UUID) -> None:
    stub("B3.4")


@org_router.get(
    "/campaigns",
    operation_id="listOrgCampaigns",
    summary="The organisation's campaigns, every status",
    response_model=OrgCampaignListResponse,
    openapi_extra=roadmap("B4.1"),
)
async def list_org_campaigns() -> None:
    stub("B4.1")


@org_router.post(
    "/campaigns",
    operation_id="createCampaign",
    summary="Create a campaign (draft)",
    description="Items must add up to the target, which is their sum. Only a verified "
    "organisation can later submit it.",
    response_model=OrgCampaignResponse,
    status_code=201,
    responses=errors(422),
    openapi_extra=roadmap("B4.1"),
)
async def create_campaign(body: CampaignCreate) -> None:
    stub("B4.1")


@org_router.patch(
    "/campaigns/{campaign_id}",
    operation_id="editCampaign",
    summary="Edit a draft",
    description="After the first donation the target and items are locked (CAMPAIGN_LOCKED).",
    response_model=OrgCampaignResponse,
    responses=errors(404, 409, 422),
    openapi_extra=roadmap("B4.3"),
)
async def edit_campaign(campaign_id: UUID, body: CampaignEdit) -> None:
    stub("B4.3")


@org_router.post(
    "/campaigns/{campaign_id}/submit",
    operation_id="submitCampaign",
    summary="Submit for review",
    response_model=OrgCampaignResponse,
    responses=errors(404, 409),
    openapi_extra=roadmap("B4.2"),
)
async def submit_campaign(campaign_id: UUID) -> None:
    stub("B4.2")


@org_router.post(
    "/campaigns/{campaign_id}/close",
    operation_id="closeCampaign",
    summary="Close a campaign early",
    response_model=OrgCampaignResponse,
    responses=errors(404, 409),
    openapi_extra=roadmap("B4.4"),
)
async def close_campaign(campaign_id: UUID) -> None:
    stub("B4.4")
