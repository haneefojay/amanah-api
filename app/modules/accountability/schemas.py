"""Expenses, evidence, campaign updates and witness confirmations (B8, B9)."""

from enum import StrEnum
from typing import Annotated, Self
from uuid import UUID

from pydantic import Field, model_validator

from app.core.schemas import (
    ContractModel,
    Email,
    ImageUrl,
    Kobo,
    Phone,
    PositiveKobo,
    Text,
    Timestamp,
)


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


class ExpenseCreate(ContractModel):
    item_id: UUID | None = None
    description: Text
    vendor_name: Text
    amount: PositiveKobo
    spent_at: Timestamp
    receipt_evidence_id: UUID | None = Field(
        default=None, description="An evidence upload of type RECEIPT."
    )


class ExpenseResponse(ContractModel):
    data: Expense


class EvidenceType(StrEnum):
    RECEIPT = "RECEIPT"
    PHOTO = "PHOTO"


class EvidenceUpload(ContractModel):
    """Describes the multipart form of POST /api/org/campaigns/{id}/evidence (B8.2)."""

    file: Annotated[str, Field(json_schema_extra={"format": "binary"})]
    type: EvidenceType
    item_id: UUID | None = None
    expense_id: UUID | None = None
    latitude: Annotated[float, Field(ge=-90, le=90)] | None = None
    longitude: Annotated[float, Field(ge=-180, le=180)] | None = None
    captured_at_client: Timestamp | None = None

    @model_validator(mode="after")
    def _coordinates_come_together(self) -> Self:
        if (self.latitude is None) != (self.longitude is None):
            msg = "Latitude and longitude come together"
            raise ValueError(msg)
        return self


class EvidenceCreated(ContractModel):
    id: UUID
    type: EvidenceType
    image_url: ImageUrl
    thumbnail_url: ImageUrl
    uploaded_at_server: Timestamp


class EvidenceCreatedResponse(ContractModel):
    data: EvidenceCreated


class UpdateCreate(ContractModel):
    body: Annotated[Text, Field(max_length=2000)]
    image_urls: list[ImageUrl] = Field(default_factory=list, max_length=6)


class UpdateCreatedResponse(ContractModel):
    data: CampaignUpdate


class WitnessAssign(ContractModel):
    name: Text
    email: Email
    phone: Phone | None = None


class WitnessAssigned(ContractModel):
    assignment_id: UUID
    witness_name: Text


class WitnessAssignedResponse(ContractModel):
    data: WitnessAssigned


class WitnessCampaign(ContractModel):
    id: UUID
    slug: Text
    title: Text
    organisation_name: Text
    pending_items: int = Field(ge=0, description="Items still waiting for this witness.")


class WitnessCampaignListResponse(ContractModel):
    data: list[WitnessCampaign]


class WitnessDecisionRequest(ContractModel):
    status: WitnessDecision
    comment: Text | None = None

    @model_validator(mode="after")
    def _dispute_needs_comment(self) -> Self:
        if self.status is WitnessDecision.DISPUTED and self.comment is None:
            msg = "A dispute needs a comment"
            raise ValueError(msg)
        return self


class WitnessDecisionResponse(ContractModel):
    data: WitnessConfirmation
