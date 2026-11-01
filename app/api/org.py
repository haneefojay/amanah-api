"""Organisation dashboard endpoints (ORG_ADMIN, own organisation only). Contract stubs."""

from uuid import UUID

from fastapi import APIRouter, Request

from app.api.support import errors, requires_session, roadmap, stub
from app.schemas.org import (
    CampaignCreate,
    CampaignEdit,
    EvidenceCreatedResponse,
    ExpenseCreate,
    ExpenseResponse,
    OrgCampaignListResponse,
    OrgCampaignResponse,
    UpdateCreate,
    UpdateCreatedResponse,
    WitnessAssign,
    WitnessAssignedResponse,
)

router = APIRouter(
    prefix="/api/org",
    tags=["organisation"],
    dependencies=requires_session,
    responses=errors(401, 403),
)


@router.get(
    "/campaigns",
    operation_id="listOrgCampaigns",
    summary="The organisation's campaigns, every status",
    response_model=OrgCampaignListResponse,
    openapi_extra=roadmap("B4.1"),
)
async def list_org_campaigns() -> None:
    stub("B4.1")


@router.post(
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


@router.patch(
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


@router.post(
    "/campaigns/{campaign_id}/submit",
    operation_id="submitCampaign",
    summary="Submit for review",
    response_model=OrgCampaignResponse,
    responses=errors(404, 409),
    openapi_extra=roadmap("B4.2"),
)
async def submit_campaign(campaign_id: UUID) -> None:
    stub("B4.2")


@router.post(
    "/campaigns/{campaign_id}/close",
    operation_id="closeCampaign",
    summary="Close a campaign early",
    response_model=OrgCampaignResponse,
    responses=errors(404, 409),
    openapi_extra=roadmap("B4.4"),
)
async def close_campaign(campaign_id: UUID) -> None:
    stub("B4.4")


@router.post(
    "/campaigns/{campaign_id}/expenses",
    operation_id="logExpense",
    summary="Log an expense",
    description="Total expenses can never exceed the amount raised (EXPENSE_EXCEEDS_RAISED).",
    response_model=ExpenseResponse,
    status_code=201,
    responses=errors(404, 409, 422),
    openapi_extra=roadmap("B8.3"),
)
async def log_expense(campaign_id: UUID, body: ExpenseCreate) -> None:
    stub("B8.3")


@router.post(
    "/campaigns/{campaign_id}/evidence",
    operation_id="uploadEvidence",
    summary="Upload a receipt or an evidence photo",
    description="Multipart form (see the request body). The server's upload time is "
    "authoritative; the phone's capture time and location are stored as given. Images only.",
    response_model=EvidenceCreatedResponse,
    status_code=201,
    responses=errors(404, 413, 415, 422),
    openapi_extra={
        **roadmap("B8.2"),
        "requestBody": {
            "required": True,
            "content": {
                "multipart/form-data": {
                    "schema": {"$ref": "#/components/schemas/EvidenceUpload"},
                }
            },
        },
    },
)
async def upload_evidence(campaign_id: UUID, request: Request) -> None:
    stub("B8.2")


@router.post(
    "/campaigns/{campaign_id}/updates",
    operation_id="postUpdate",
    summary="Post an update to the timeline",
    response_model=UpdateCreatedResponse,
    status_code=201,
    responses=errors(404, 422),
    openapi_extra=roadmap("B9.3"),
)
async def post_update(campaign_id: UUID, body: UpdateCreate) -> None:
    stub("B9.3")


@router.post(
    "/campaigns/{campaign_id}/witnesses",
    operation_id="assignWitness",
    summary="Assign a witness",
    description="A witness cannot be an admin of the organisation (WITNESS_CONFLICT).",
    response_model=WitnessAssignedResponse,
    status_code=201,
    responses=errors(404, 409, 422),
    openapi_extra=roadmap("B9.1"),
)
async def assign_witness(campaign_id: UUID, body: WitnessAssign) -> None:
    stub("B9.1")
