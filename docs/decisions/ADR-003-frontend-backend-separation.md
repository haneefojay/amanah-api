# ADR-003: Separate backend service and contract-first frontend development

- **Status:** Accepted
- **Date:** 2026-10-18
- **Deciders:** Project owner
- **Related:** spec §8; FRONTEND_ROADMAP F0.4; BACKEND_ROADMAP B0.3; ADR-004

## Context

An initial proposal used Next.js route handlers as the backend. The project owner rejected this as not scalable enough and wants a separate backend, whose stack will be decided later (ADR-004). Frontend work must not stall in the meantime, and the deadline is 1 November 2026.

## Options considered

### Option A: Next.js full-stack (route handlers and server actions as the backend)

- Pros: one codebase and deployment; fastest to start.
- Cons: couples business logic to the UI framework; harder to scale and staff independently; rejected by the project owner.

### Option B: Separate backend service, frontend waits for it

- Pros: clean separation.
- Cons: frontend is blocked for days. Unacceptable with a two-week deadline.

### Option C: Separate backend service with contract-first, mock-backed frontend development

- Pros: clean separation, and both tracks progress in parallel; the mock doubles as test fixtures.
- Cons: risk of contract drift between the mock and the real API. Mitigated by runtime Zod validation and the B0.3 OpenAPI contract.

## Decision

Option C.

- The backend is a **separate service** exposing a JSON HTTP API (paths as in spec §8).
- The frontend calls it only through `src/lib/api` (`apiFetch`). Every response is validated with **Zod** schemas in `src/lib/api/schemas.ts`.
- **MSW** handlers in `src/mocks/handlers.ts` implement the draft contract. They are used by unit and component tests (`msw/node`) and served over HTTP for local development by `npm run mock:api` (port 4000).
- Once the backend publishes OpenAPI (B0.3), frontend types are generated from it and the Zod schemas are reconciled. The OpenAPI document becomes the source of truth.
- No secrets or business rules live in the frontend. The frontend mirrors rules only for user experience (for example a client-side check that items total the target), and the backend always enforces them.

## Rationale

This keeps the owner's architecture while letting frontend features reach "Done (mocked)" now and integrate as backend items land.

## Consequences

- Positive: parallel progress; deterministic tests; contract drift fails loudly (`CONTRACT_MISMATCH`).
- Negative or risks: cross-origin calls need CORS with credentials, and cookie-based auth needs careful `SameSite` and domain setup (B2.1, B12.1). Keeping the mock and the real API in sync is ongoing work.
- Follow-up: B0.3 (OpenAPI), F0.4 reconciliation, B12.1 (CORS).
