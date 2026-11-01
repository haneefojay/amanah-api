"""Building blocks shared by every contract model (cross-cutting, owned by no module)."""

from typing import Annotated, Any
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints
from pydantic.alias_generators import to_camel

# Money is integer kobo (1 naira = 100 kobo). Never a float (spec section 9).
Kobo = Annotated[int, Field(ge=0, description="Amount in kobo (integer). 100 kobo = 1 naira.")]
PositiveKobo = Annotated[int, Field(gt=0, description="Amount in kobo (integer), above zero.")]

# Timestamps are timezone-aware and serialised as ISO 8601 UTC ("2026-11-01T21:00:00Z").
Timestamp = AwareDatetime

# An absolute URL (object storage) or a root-relative path served by the frontend.
ImageUrl = Annotated[
    str,
    StringConstraints(min_length=1, pattern=r"^(https?://\S+|/[^/\s]\S*)$"),
    Field(description="Absolute URL, or a root-relative path such as /images/x.jpg."),
]

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

# A plain pattern keeps the dependency list short; the service layer does real validation.
Email = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, to_lower=True, max_length=254, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    ),
    Field(description="Email address."),
]
Phone = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, min_length=7, max_length=20, pattern=r"^\+?[0-9 ()-]+$"
    ),
    Field(description="Phone number, for example +2348012345678."),
]


class ContractModel(BaseModel):
    """Base for every request and response model: camelCase on the wire, snake_case in Python."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="forbid")


class ApiErrorDetail(ContractModel):
    code: str = Field(description="SCREAMING_SNAKE code. See info.x-error-codes.")
    message: str = Field(description="A message safe to show to a person.")
    details: dict[str, Any] | None = Field(
        default=None,
        description="Extra machine-readable data, for example availableAmount on "
        "AMOUNT_EXCEEDS_AVAILABLE.",
    )


class ApiError(ContractModel):
    """The standard error envelope used by every non-2xx response."""

    error: ApiErrorDetail


class PageMeta(ContractModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=1)


class IdName(ContractModel):
    id: UUID
    name: Text
