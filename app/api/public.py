"""Public endpoints: browsing, checkout, donation status, payment webhook, registration.

Contract stubs: each returns 501 NOT_IMPLEMENTED until its roadmap item (x-roadmap) is built.
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Header, Query

from app.api.support import errors, roadmap, stub
from app.schemas.donations import (
    CheckoutRequest,
    CheckoutResponse,
    DonationStatusResponse,
    WebhookAck,
    WebhookEvent,
)
from app.schemas.org import OrganisationRegisteredResponse, OrganisationRegistration
from app.schemas.public import (
    CampaignDetailResponse,
    CampaignListResponse,
    OrganisationProfileResponse,
)

router = APIRouter(prefix="/api", tags=["public"])


@router.get(
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


@router.get(
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


@router.get(
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


@router.post(
    "/organisations",
    operation_id="registerOrganisation",
    summary="Register an organisation and its first admin",
    description="Creates the organisation as PENDING and its admin account. A platform admin "
    "verifies it before it can publish.",
    response_model=OrganisationRegisteredResponse,
    status_code=201,
    responses=errors(409, 422, 429),
    openapi_extra=roadmap("B3.1"),
)
async def register_organisation(body: OrganisationRegistration) -> None:
    stub("B3.1")


@router.post(
    "/campaigns/{campaign_id}/checkout",
    operation_id="createCheckout",
    summary="Reserve an amount and start the payment",
    description="Creates a reservation inside a locked transaction (spec 4.2) and initialises the "
    "payment. Answers 409 AMOUNT_EXCEEDS_AVAILABLE (with details.availableAmount), TARGET_REACHED "
    "or CAMPAIGN_NOT_ACCEPTING when the donation cannot be taken.",
    response_model=CheckoutResponse,
    status_code=201,
    responses=errors(404, 409, 422, 429),
    openapi_extra=roadmap("B6.1"),
)
async def create_checkout(campaign_id: UUID, body: CheckoutRequest) -> None:
    stub("B6.1")


@router.get(
    "/donations/{reference}",
    operation_id="getDonation",
    summary="Donation status for the result page",
    description="The reference is the reservation ID. Never includes the donor's email or phone. "
    "The page must not claim success before status is CONFIRMED.",
    response_model=DonationStatusResponse,
    responses=errors(404),
    openapi_extra=roadmap("B7.5"),
)
async def get_donation(reference: UUID) -> None:
    stub("B7.5")


@router.post(
    "/webhooks/payments",
    operation_id="receivePaymentWebhook",
    summary="Payment provider webhook",
    description="Verifies the signature header, then the provider's verify endpoint, before "
    "confirming anything. Idempotent: safe to replay.",
    response_model=WebhookAck,
    responses=errors(400),
    openapi_extra=roadmap("B7.3"),
)
async def receive_payment_webhook(
    body: WebhookEvent,
    x_paystack_signature: Annotated[str | None, Header()] = None,
) -> None:
    stub("B7.3")
