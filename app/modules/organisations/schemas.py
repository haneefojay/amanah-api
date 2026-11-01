"""Organisation registration and summary models (B3)."""

from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import Field

from app.core.schemas import (
    ContractModel,
    Email,
    Phone,
    Text,
    Timestamp,
)


class OrganisationSummary(ContractModel):
    id: UUID
    name: Text
    city: Text
    state: Text
    verified_at: Timestamp = Field(description="Only verified organisations are public.")
    campaign_count: int = Field(ge=0, description="Public campaigns.")
    ended_count: int = Field(ge=0, description="Closed or completed campaigns.")
    completed_count: int = Field(ge=0)


class VerificationStatus(StrEnum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


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
