# API contract

The contract is the OpenAPI document generated from the Pydantic models in each module's `schemas.py` (`app/modules/<module>/schemas.py`). The committed copy is [`openapi.json`](../openapi.json); the running service serves it at `/api/openapi.json` and the interactive docs at `/api/docs`.

Every route in the spec (section 8) already exists as a **stub** that answers `501 NOT_IMPLEMENTED`. Each carries `x-roadmap` (the item that builds it) and `x-implemented: false`. When an item ships, replace the stub, set `x-implemented` to `true` (drop the `stub(...)` call) and regenerate.

## Regenerating

```
uv run python scripts/export_openapi.py          # rewrite openapi.json
uv run python scripts/export_openapi.py --check  # fail if it is stale (the tests run this)
```

Never edit `openapi.json` by hand. Any change to a schema or route needs a regenerated file in the same commit.

## Conventions

| Topic | Rule |
| --- | --- |
| JSON keys | camelCase on the wire, snake_case in Python (`alias_generator`). Unknown fields in a request are rejected. |
| Money | Integer kobo, never a float. Fields end in `Amount`. |
| Timestamps | UTC, ISO 8601 with an offset (`2026-11-01T09:30:00Z`). |
| IDs | UUIDs. Campaigns are addressed publicly by `slug`. |
| Success | `{ "data": ... }`. Lists add `meta` (page, pageSize, total, totalPages) where paged. |
| Errors | `{ "error": { "code": "SCREAMING_SNAKE", "message": "...", "details"?: {...} } }` |
| Auth | httpOnly session cookie `amanah_session` (ADR-011). Public routes need nothing; `/api/org/*`, `/api/witness/*` and `/api/admin/*` declare the `sessionCookie` scheme and answer 401 or 403. |
| Privacy | Public responses and the donation status never include donor email or phone. |

## Error codes

The full catalogue (status and meaning) is published in the document as `info.x-error-codes` and defined in `app/core/error_codes.py`. The ones the frontend depends on, which must keep their exact names: `AMOUNT_EXCEEDS_AVAILABLE` (with `details.availableAmount`), `TARGET_REACHED`, `CAMPAIGN_NOT_ACCEPTING`, `WITNESS_CONFLICT`. Add a code to the catalogue before using it.

## Keeping the frontend in step

`tests/contract/fixtures/frontend-mock-payloads.json` is a snapshot of what the frontend's mock API serves. `tests/contract/test_frontend_payloads.py` validates it against the models, so a drift in either direction shows up here. The frontend then generates its TypeScript types from `openapi.json` (a follow-up frontend change).

If a model change breaks the snapshot, the contract changed: update the frontend schemas and refresh the snapshot in the same piece of work.
