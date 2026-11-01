"""Campaign models: the public catalogue and the organisation dashboard (B4, B5)."""

from enum import StrEnum
from typing import Annotated, Self
from uuid import UUID

from pydantic import Field, model_validator

from app.core.schemas import (
    ContractModel,
    IdName,
    ImageUrl,
    Kobo,
    PageMeta,
    PositiveKobo,
    Text,
    Timestamp,
)
from app.modules.accountability import (
    CampaignUpdate,
    EvidencePhoto,
    Expense,
    WitnessConfirmation,
    WitnessDecision,
)
from app.modules.organisations import (
    OrganisationSummary,
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


class ItemInput(ContractModel):
    name: Text
    quantity: int = Field(gt=0)
    unit_cost: PositiveKobo


class CampaignCreate(ContractModel):
    title: Annotated[Text, Field(max_length=140)]
    purpose: Text
    description: Annotated[list[Text], Field(min_length=1)]
    cover_image_url: ImageUrl | None = None
    ends_at: Timestamp | None = None
    items: Annotated[list[ItemInput], Field(min_length=1)]


class CampaignEdit(ContractModel):
    """Every field is optional. The target and items are locked after the first donation."""

    title: Annotated[Text, Field(max_length=140)] | None = None
    purpose: Text | None = None
    description: Annotated[list[Text], Field(min_length=1)] | None = None
    cover_image_url: ImageUrl | None = None
    ends_at: Timestamp | None = None
    items: Annotated[list[ItemInput], Field(min_length=1)] | None = None


class OrgCampaign(ContractModel):
    id: UUID
    slug: Text
    title: Text
    status: CampaignStatus
    target_amount: Kobo
    raised_amount: Kobo
    review_note: Text | None = Field(description="Why an admin rejected it, if they did.")
    updated_at: Timestamp


class OrgCampaignResponse(ContractModel):
    data: OrgCampaign


class OrgCampaignListResponse(ContractModel):
    data: list[OrgCampaign]
