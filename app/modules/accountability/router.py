"""Expenses, evidence, updates and witness confirmation (B8, B9). Contract stubs."""

from uuid import UUID

from fastapi import APIRouter, Request

from app.core.security import requires_session
from app.core.stubs import errors, roadmap, stub
from app.modules.accountability.schemas import (
    EvidenceCreatedResponse,
    ExpenseCreate,
    ExpenseResponse,
    UpdateCreate,
    UpdateCreatedResponse,
    WitnessAssign,
    WitnessAssignedResponse,
    WitnessCampaignListResponse,
    WitnessDecisionRequest,
    WitnessDecisionResponse,
)

org_router = APIRouter(
    prefix="/api/org",
    tags=["organisation"],
    dependencies=requires_session,
    responses=errors(401, 403),
)

witness_router = APIRouter(
    prefix="/api/witness",
    tags=["witness"],
    dependencies=requires_session,
    responses=errors(401, 403),
)


@org_router.post(
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


@org_router.post(
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


@org_router.post(
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


@org_router.post(
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


@witness_router.get(
    "/campaigns",
    operation_id="listWitnessCampaigns",
    summary="Campaigns assigned to the signed-in witness",
    response_model=WitnessCampaignListResponse,
    openapi_extra=roadmap("B9.2"),
)
async def list_witness_campaigns() -> None:
    stub("B9.2")


@witness_router.post(
    "/items/{item_id}/confirm",
    operation_id="confirmItem",
    summary="Confirm or dispute delivery of an item",
    description="A dispute needs a comment. A disputed item can never be shown as delivered.",
    response_model=WitnessDecisionResponse,
    responses=errors(404, 409, 422),
    openapi_extra=roadmap("B9.2"),
)
async def confirm_item(item_id: UUID, body: WitnessDecisionRequest) -> None:
    stub("B9.2")
