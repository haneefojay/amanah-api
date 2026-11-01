"""Platform admin endpoints (PLATFORM_ADMIN, B10). Contract stubs."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.core.security import requires_session
from app.core.stubs import errors, roadmap, stub
from app.modules.admin.schemas import (
    AdminCampaignListResponse,
    AdminOrganisationListResponse,
    CampaignReview,
    OrganisationVerification,
    OrganisationVerificationResponse,
)
from app.modules.audit import AuditLogResponse
from app.modules.campaigns import (
    CampaignStatus,
    OrgCampaignResponse,
)
from app.modules.donations import (
    ExcessListResponse,
    ExcessResolution,
    ExcessResolutionResponse,
)
from app.modules.organisations import (
    VerificationStatus,
)

admin_router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=requires_session,
    responses=errors(401, 403),
)


@admin_router.get(
    "/organisations",
    operation_id="listAdminOrganisations",
    summary="Organisations, newest first (the verification queue)",
    response_model=AdminOrganisationListResponse,
    openapi_extra=roadmap("B10.1"),
)
async def list_admin_organisations(
    status: VerificationStatus | None = VerificationStatus.PENDING,
) -> None:
    stub("B10.1")


@admin_router.post(
    "/organisations/{organisation_id}/verify",
    operation_id="verifyOrganisation",
    summary="Verify or reject an organisation",
    description="Rejection needs a reason.",
    response_model=OrganisationVerificationResponse,
    responses=errors(404, 409, 422),
    openapi_extra=roadmap("B3.3"),
)
async def verify_organisation(organisation_id: UUID, body: OrganisationVerification) -> None:
    stub("B3.3")


@admin_router.get(
    "/campaigns",
    operation_id="listAdminCampaigns",
    summary="Campaigns, newest first (the review queue)",
    response_model=AdminCampaignListResponse,
    openapi_extra=roadmap("B10.2"),
)
async def list_admin_campaigns(
    status: Annotated[CampaignStatus | None, Query()] = CampaignStatus.PENDING_REVIEW,
) -> None:
    stub("B10.2")


@admin_router.post(
    "/campaigns/{campaign_id}/review",
    operation_id="reviewCampaign",
    summary="Approve or reject a campaign",
    description="Approval makes it LIVE. Rejection needs a reason and returns it to the "
    "organisation.",
    response_model=OrgCampaignResponse,
    responses=errors(404, 409, 422),
    openapi_extra=roadmap("B4.2"),
)
async def review_campaign(campaign_id: UUID, body: CampaignReview) -> None:
    stub("B4.2")


@admin_router.get(
    "/excess",
    operation_id="listExcess",
    summary="Excess records, newest first",
    response_model=ExcessListResponse,
    openapi_extra=roadmap("B10.3"),
)
async def list_excess() -> None:
    stub("B10.3")


@admin_router.patch(
    "/excess/{excess_id}",
    operation_id="resolveExcess",
    summary="Resolve an excess record",
    response_model=ExcessResolutionResponse,
    responses=errors(404, 409, 422),
    openapi_extra=roadmap("B7.4"),
)
async def resolve_excess(excess_id: UUID, body: ExcessResolution) -> None:
    stub("B7.4")


@admin_router.get(
    "/audit-log",
    operation_id="listAuditLog",
    summary="The append-only audit log, newest first",
    response_model=AuditLogResponse,
    openapi_extra=roadmap("B10.4"),
)
async def list_audit_log(
    entity_type: Annotated[str | None, Query(alias="entityType")] = None,
    entity_id: Annotated[UUID | None, Query(alias="entityId")] = None,
) -> None:
    stub("B10.4")
