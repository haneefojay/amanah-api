"""Public read models: campaigns, organisations and their accountability data (spec 5 to 7).

These mirror the frontend's `src/lib/api/schemas.ts` field for field. A contract test validates
the frontend's mock payloads against them, so drift fails the build.
"""

from enum import StrEnum
from typing import Annotated, Self
from uuid import UUID

from pydantic import Field, model_validator

from app.schemas.common import (
    ContractModel,
    IdName,
    ImageUrl,
    Kobo,
    PageMeta,
    Text,
    Timestamp,
)


class CampaignStatus(StrEnum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    REJECTED = "REJECTED"
    LIVE = "LIVE"
    FUNDED = "FUNDED"
    CLOSED = "CLOSED"
    COMPLETED = "COMPLETED"


class ItemDisplayStatus(StrEnum):
    NEEDED = "NEEDED"
    PURCHASED = "PURCHASED"
    DELIVERED = "DELIVERED"
    DISPUTED = "DISPUTED"


class CampaignSummary(ContractModel):
    id: UUID
    slug: Text
    title: Text
    organisation_id: UUID
    organisation_name: Text
    city: Text
    state: Text
    cover_image_url: ImageUrl | None
    status: CampaignStatus
    target_amount: Kobo
    raised_amount: Kobo
    available_amount: Kobo = Field(
        description="target - raised - active reservations (spec 4.2). The only figure that "
        "decides whether a donation can be offered."
    )


class CampaignFilters(ContractModel):
    cities: list[Text]
    organisations: list[IdName]


class CampaignListResponse(ContractModel):
    """GET /api/campaigns (B5.1): a page of public campaigns plus the values filters can offer."""

    data: list[CampaignSummary]
    meta: PageMeta
    filters: CampaignFilters


class OrganisationSummary(ContractModel):
    id: UUID
    name: Text
    city: Text
    state: Text
    verified_at: Timestamp = Field(description="Only verified organisations are public.")
    campaign_count: int = Field(ge=0, description="Public campaigns.")
    ended_count: int = Field(ge=0, description="Closed or completed campaigns.")
    completed_count: int = Field(ge=0)


class WitnessDecision(StrEnum):
    CONFIRMED = "CONFIRMED"
    DISPUTED = "DISPUTED"


class WitnessConfirmation(ContractModel):
    """The independent witness's word on one item (spec 7). Witnesses are named publicly."""

    status: WitnessDecision
    witness_name: Text
    confirmed_at: Timestamp
    comment: Text | None

    @model_validator(mode="after")
    def _dispute_needs_comment(self) -> Self:
        if self.status is WitnessDecision.DISPUTED and self.comment is None:
            msg = "A dispute needs the witness's comment"
            raise ValueError(msg)
        return self


class CampaignItem(ContractModel):
    """One thing the campaign buys. Items add up to the campaign target (spec 4.1)."""

    id: UUID
    name: Text
    quantity: int = Field(gt=0)
    unit_cost: Kobo
    total_cost: Kobo
    status: ItemDisplayStatus
    confirmation: WitnessConfirmation | None

    @model_validator(mode="after")
    def _disputed_items_agree(self) -> Self:
        disputed_item = self.status is ItemDisplayStatus.DISPUTED
        disputed_confirmation = (
            self.confirmation is not None and self.confirmation.status is WitnessDecision.DISPUTED
        )
        if disputed_item != disputed_confirmation:
            msg = "Disputed items and disputed confirmations must agree"
            raise ValueError(msg)
        return self


class Receipt(ContractModel):
    id: UUID
    image_url: ImageUrl
    thumbnail_url: ImageUrl
    uploaded_at_server: Timestamp = Field(description="Authoritative upload time (spec 7).")


class Expense(ContractModel):
    id: UUID
    description: Text
    vendor_name: Text
    amount: Kobo
    spent_at: Timestamp
    item_id: UUID | None = Field(description="The item it paid for; null for a general cost.")
    receipt: Receipt | None


class EvidencePhoto(ContractModel):
    id: UUID
    image_url: ImageUrl
    thumbnail_url: ImageUrl
    item_id: UUID | None
    expense_id: UUID | None
    latitude: Annotated[float, Field(ge=-90, le=90)] | None
    longitude: Annotated[float, Field(ge=-180, le=180)] | None
    captured_at_client: Timestamp | None = Field(
        description="What the phone said. Secondary to uploadedAtServer."
    )
    uploaded_at_server: Timestamp

    @model_validator(mode="after")
    def _coordinates_come_together(self) -> Self:
        if (self.latitude is None) != (self.longitude is None):
            msg = "Latitude and longitude come together"
            raise ValueError(msg)
        return self


class CampaignUpdate(ContractModel):
    id: UUID
    body: Text
    images: list[ImageUrl]
    posted_at: Timestamp


class CampaignDetail(CampaignSummary):
    """GET /api/campaigns/{slug} (B5.2). Spent is never sent: it is the sum of the expenses."""

    purpose: Text
    description: Annotated[list[Text], Field(min_length=1, description="Paragraphs of text.")]
    published_at: Timestamp
    ends_at: Timestamp | None
    items: list[CampaignItem]
    organisation: OrganisationSummary
    expenses: list[Expense] = Field(description="Newest first.")
    evidence: list[EvidencePhoto] = Field(description="Newest first, by upload time.")
    updates: list[CampaignUpdate] = Field(description="Newest first.")

    @model_validator(mode="after")
    def _expenses_within_raised(self) -> Self:
        if sum(e.amount for e in self.expenses) > self.raised_amount:
            msg = "Expenses can't exceed the amount raised"
            raise ValueError(msg)
        return self


class CampaignDetailResponse(ContractModel):
    data: CampaignDetail


class OrganisationProfile(OrganisationSummary):
    """GET /api/organisations/{id} (B3.4). Type and registration number are never public."""

    address: Text
    cover_image_url: ImageUrl | None
    raised_amount: Kobo = Field(description="Total raised across its public campaigns.")
    campaigns: list[CampaignSummary]


class OrganisationProfileResponse(ContractModel):
    data: OrganisationProfile


# Used by the donation status endpoint.
