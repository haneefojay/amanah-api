"""Witness endpoints (WITNESS, assigned campaigns only). Contract stubs."""

from uuid import UUID

from fastapi import APIRouter

from app.api.support import errors, requires_session, roadmap, stub
from app.schemas.org import (
    WitnessCampaignListResponse,
    WitnessDecisionRequest,
    WitnessDecisionResponse,
)

router = APIRouter(
    prefix="/api/witness",
    tags=["witness"],
    dependencies=requires_session,
    responses=errors(401, 403),
)


@router.get(
    "/campaigns",
    operation_id="listWitnessCampaigns",
    summary="Campaigns assigned to the signed-in witness",
    response_model=WitnessCampaignListResponse,
    openapi_extra=roadmap("B9.2"),
)
async def list_witness_campaigns() -> None:
    stub("B9.2")


@router.post(
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
