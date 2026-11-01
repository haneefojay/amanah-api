"""The error code catalogue. Every non-2xx response carries one of these in `error.code`.

The catalogue is published in the OpenAPI document as `info.x-error-codes`, so the frontend and
any other client can rely on it. Add a code here (and to docs/api-contract.md) before using it.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorCode:
    status: int
    meaning: str


CATALOGUE: dict[str, ErrorCode] = {
    # Generic
    "BAD_REQUEST": ErrorCode(400, "The request could not be understood."),
    "VALIDATION_ERROR": ErrorCode(422, "A field is missing or invalid. The message names it."),
    "UNAUTHORIZED": ErrorCode(401, "No valid session. Sign in first."),
    "INVALID_CREDENTIALS": ErrorCode(401, "Wrong email or password. Never says which."),
    "FORBIDDEN": ErrorCode(403, "Signed in, but this role or organisation may not do this."),
    "NOT_FOUND": ErrorCode(404, "No such resource, or it is not public."),
    "METHOD_NOT_ALLOWED": ErrorCode(405, "That method is not supported on this path."),
    "CONFLICT": ErrorCode(409, "The request conflicts with the current state."),
    "RATE_LIMITED": ErrorCode(429, "Too many requests. Try again later."),
    "INTERNAL_ERROR": ErrorCode(500, "Something went wrong. Nothing internal is revealed."),
    "NOT_IMPLEMENTED": ErrorCode(501, "In the contract but not built yet (see x-roadmap)."),
    # Donations (spec 4)
    "AMOUNT_EXCEEDS_AVAILABLE": ErrorCode(
        409, "More than is available. details.availableAmount says how much can be given."
    ),
    "TARGET_REACHED": ErrorCode(409, "Nothing is available: the target is reached or reserved."),
    "CAMPAIGN_NOT_ACCEPTING": ErrorCode(409, "The campaign is not live."),
    "INVALID_SIGNATURE": ErrorCode(400, "The webhook signature did not verify."),
    # Campaigns and organisations (spec 5)
    "INVALID_TRANSITION": ErrorCode(409, "That status change is not allowed from here."),
    "CAMPAIGN_LOCKED": ErrorCode(409, "The target and items cannot change after a donation."),
    "ITEMS_TARGET_MISMATCH": ErrorCode(422, "The items do not add up to the target."),
    "ORGANISATION_NOT_VERIFIED": ErrorCode(409, "Only a verified organisation can publish."),
    # Accountability (spec 6, 7)
    "EXPENSE_EXCEEDS_RAISED": ErrorCode(409, "Total expenses would exceed the amount raised."),
    "WITNESS_CONFLICT": ErrorCode(409, "A witness cannot be an admin of the organisation."),
    "FILE_TOO_LARGE": ErrorCode(413, "The file is larger than allowed."),
    "UNSUPPORTED_FILE_TYPE": ErrorCode(415, "Only image files are accepted for evidence."),
}
