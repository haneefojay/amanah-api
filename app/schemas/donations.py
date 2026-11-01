"""Checkout, payments and donation status (B6, B7). Donors are guests (spec D7)."""

from enum import StrEnum
from typing import Annotated, Any
from uuid import UUID

from pydantic import ConfigDict, Field

from app.schemas.common import ContractModel, Email, Kobo, Phone, PositiveKobo, Text, Timestamp


class CheckoutRequest(ContractModel):
    amount: PositiveKobo
    donor_name: Annotated[Text, Field(max_length=120)]
    donor_email: Email
    donor_phone: Phone


class Checkout(ContractModel):
    reference: UUID = Field(description="The reservation ID. It doubles as the payment reference.")
    authorization_url: Annotated[str, Field(description="The provider's hosted checkout page.")]
    amount: Kobo
    expires_at: Timestamp = Field(description="When the reservation is released if unpaid.")


class CheckoutResponse(ContractModel):
    data: Checkout


class DonationState(StrEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"


class DonationStatus(ContractModel):
    """Shown on the result page. It never includes the donor's email or phone."""

    reference: UUID
    status: DonationState
    amount: Kobo
    campaign_slug: Text
    campaign_title: Text
    donor_name: Text
    paid_at: Timestamp | None


class DonationStatusResponse(ContractModel):
    data: DonationStatus


class WebhookEvent(ContractModel):
    """The provider's event body, passed through as received. It is verified, not trusted."""

    model_config = ConfigDict(extra="allow")

    event: Text
    data: dict[str, Any]


class WebhookAck(ContractModel):
    received: bool = True
