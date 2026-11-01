"""Organisation dashboard, witness and platform admin models (B3, B4, B8, B9, B10)."""

from enum import StrEnum
from typing import Annotated, Self
from uuid import UUID

from pydantic import Field, model_validator

from app.schemas.common import (
    ContractModel,
    Email,
    ImageUrl,
    Kobo,
    Phone,
    PositiveKobo,
    Text,
    Timestamp,
)
from app.schemas.public import (
    CampaignStatus,
    CampaignUpdate,
    Expense,
    WitnessConfirmation,
    WitnessDecision,
)


class VerificationStatus(StrEnum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


# --- Organisation registration (B3.1) ------------------------------------------------------


class OrganisationRegistration(ContractModel):
    name: Text
    type: Annotated[Text, Field(description="For example mosque, orphanage or society.")]
    address: Text
    city: Text
    state: Text
    registration_number: Text
    contact_person: Text
    admin_name: Text
    admin_email: Email
    admin_phone: Phone
    password: Annotated[str, Field(min_length=10, max_length=256)]


class OrganisationRegistered(ContractModel):
    organisation_id: UUID
    verification_status: VerificationStatus


class OrganisationRegisteredResponse(ContractModel):
    data: OrganisationRegistered


# --- Campaigns (B4) ------------------------------------------------------------------------


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


# --- Witness (B9) --------------------------------------------------------------------------


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


# --- Platform admin (B10) ------------------------------------------------------------------


class AdminOrganisation(ContractModel):
    id: UUID
    name: Text
    city: Text
    state: Text
    verification_status: VerificationStatus
    verification_notes: Text | None
    submitted_at: Timestamp
    document_urls: list[ImageUrl] = Field(description="Signed, short-lived URLs (ADR-013).")


class AdminOrganisationListResponse(ContractModel):
    data: list[AdminOrganisation]


class VerifyDecision(StrEnum):
    VERIFY = "VERIFY"
    REJECT = "REJECT"


class OrganisationVerification(ContractModel):
    decision: VerifyDecision
    notes: Text | None = None

    @model_validator(mode="after")
    def _rejection_needs_notes(self) -> Self:
        if self.decision is VerifyDecision.REJECT and self.notes is None:
            msg = "A rejection needs a reason"
            raise ValueError(msg)
        return self


class OrganisationVerificationResult(ContractModel):
    verification_status: VerificationStatus


class OrganisationVerificationResponse(ContractModel):
    data: OrganisationVerificationResult


class ReviewDecision(StrEnum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"


class CampaignReview(ContractModel):
    decision: ReviewDecision
    reason: Text | None = None

    @model_validator(mode="after")
    def _rejection_needs_reason(self) -> Self:
        if self.decision is ReviewDecision.REJECT and self.reason is None:
            msg = "A rejection needs a reason"
            raise ValueError(msg)
        return self


class AdminCampaign(ContractModel):
    id: UUID
    slug: Text
    title: Text
    organisation_name: Text
    status: CampaignStatus
    target_amount: Kobo
    submitted_at: Timestamp | None


class AdminCampaignListResponse(ContractModel):
    data: list[AdminCampaign]


class ExcessStatus(StrEnum):
    PENDING_RETURN = "PENDING_RETURN"
    RETURNED = "RETURNED"
    SENT_TO_BAYT_AL_MAL = "SENT_TO_BAYT_AL_MAL"


class ExcessRecord(ContractModel):
    id: UUID
    donation_id: UUID
    campaign_title: Text
    amount: PositiveKobo
    status: ExcessStatus
    notes: Text | None
    created_at: Timestamp


class ExcessListResponse(ContractModel):
    data: list[ExcessRecord]


class ExcessResolution(ContractModel):
    status: Annotated[
        ExcessStatus, Field(description="RETURNED or SENT_TO_BAYT_AL_MAL. Not PENDING_RETURN.")
    ]
    notes: Text

    @model_validator(mode="after")
    def _must_resolve(self) -> Self:
        if self.status is ExcessStatus.PENDING_RETURN:
            msg = "Resolve to RETURNED or SENT_TO_BAYT_AL_MAL"
            raise ValueError(msg)
        return self


class ExcessResolutionResponse(ContractModel):
    data: ExcessRecord


class AuditEntry(ContractModel):
    id: UUID
    actor_id: UUID | None
    action: Text
    entity_type: Text
    entity_id: UUID | None
    payload: dict[str, object]
    created_at: Timestamp


class AuditLogResponse(ContractModel):
    data: list[AuditEntry]
