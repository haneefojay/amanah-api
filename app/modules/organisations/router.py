"""Organisation registration (B3.1). Contract stub."""

from fastapi import APIRouter

from app.core.stubs import errors, roadmap, stub
from app.modules.organisations.schemas import (
    OrganisationRegisteredResponse,
    OrganisationRegistration,
)

public_router = APIRouter(prefix="/api", tags=["public"])


@public_router.post(
    "/organisations",
    operation_id="registerOrganisation",
    summary="Register an organisation and its first admin",
    description="Creates the organisation as PENDING and its admin account. A platform admin "
    "verifies it before it can publish.",
    response_model=OrganisationRegisteredResponse,
    status_code=201,
    responses=errors(409, 422, 429),
    openapi_extra=roadmap("B3.1"),
)
async def register_organisation(body: OrganisationRegistration) -> None:
    stub("B3.1")
