"""Platform admin request and response models (B10)."""

from enum import StrEnum
from typing import Self
from uuid import UUID

from pydantic import Field, model_validator

from app.core.schemas import (
    ContractModel,
    ImageUrl,
    Kobo,
    Text,
    Timestamp,
)
from app.modules.campaigns import (
    CampaignStatus,
)
from app.modules.organisations import (
    VerificationStatus,
)


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
