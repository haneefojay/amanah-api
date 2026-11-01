"""Authentication and the signed-in user (ADR-011, B2.1, B2.3)."""

from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import Field

from app.schemas.common import ContractModel, Email, IdName, Text


class UserRole(StrEnum):
    ORG_ADMIN = "ORG_ADMIN"
    WITNESS = "WITNESS"
    PLATFORM_ADMIN = "PLATFORM_ADMIN"


class LoginRequest(ContractModel):
    email: Email
    password: Annotated[str, Field(min_length=1, max_length=256)]


class CurrentUser(ContractModel):
    id: UUID
    name: Text
    email: Email
    role: UserRole
    organisations: list[IdName]


class CurrentUserResponse(ContractModel):
    data: CurrentUser
