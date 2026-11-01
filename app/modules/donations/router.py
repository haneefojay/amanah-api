"""Checkout, donation status and the payment webhook (B6, B7). Contract stubs."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Header

from app.core.stubs import errors, roadmap, stub
from app.modules.donations.schemas import (
    CheckoutRequest,
    CheckoutResponse,
    DonationStatusResponse,
    WebhookAck,
    WebhookEvent,
)

public_router = APIRouter(prefix="/api", tags=["public"])


@public_router.post(
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


@public_router.get(
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


@public_router.post(
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
