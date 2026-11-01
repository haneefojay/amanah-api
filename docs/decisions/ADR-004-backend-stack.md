# ADR-004: Backend technology stack

- **Status:** Accepted
- **Date:** 2026-10-18 (proposed), 2026-11-01 (accepted)
- **Deciders:** Project owner (Haneef)
- **Related:** spec §4.2, §8 (D5), §9; BACKEND_ROADMAP B0; ADR-003; ADR-011, ADR-012, ADR-013

## Context

The backend must be a separate, scalable service (ADR-003). Hard requirements from the spec that any stack must meet:

- **PostgreSQL** with row-level locking (`SELECT … FOR UPDATE`) inside transactions, for the donation cap (§4.2);
- integer money handling (kobo) end to end;
- verified, idempotent payment webhooks (Paystack);
- object storage for receipts, evidence and documents;
- a scheduled or background job for reservation expiry;
- an OpenAPI contract for the frontend (B0.3);
- buildable and deployable by the team before 1 November 2026.

## Options considered

To be completed with the team. Starting candidates:

### Option A: Node.js (NestJS or Fastify) with TypeScript, Prisma or Drizzle, PostgreSQL

- Pros: same language as the frontend, so types and validation can be shared; mature Paystack examples; NestJS gives structure (modules, guards, OpenAPI generation).
- Cons: NestJS has a learning curve. ORM row-lock support needs raw SQL in places.

### Option B: Python (Django REST Framework or FastAPI), PostgreSQL

- Pros: Django gives an admin, auth and migrations out of the box; `select_for_update()` is first-class; FastAPI auto-generates OpenAPI.
- Cons: a second language for the team; type sharing with the frontend only via generated OpenAPI types.

### Option C: Go (chi or Echo, sqlc), PostgreSQL

- Pros: performance and simple deployment; explicit SQL makes locking clear.
- Cons: slowest to build features with under deadline pressure.

### Option D: Laravel (PHP), PostgreSQL

- Pros: batteries included (auth, queues, storage, scheduler); popular in Nigeria.
- Cons: a second language; less type sharing.

Hosting candidates (decide alongside): Render, Railway, Fly.io, or a VPS, with managed PostgreSQL (Supabase, Neon or the host's own) and storage (Supabase Storage, Cloudflare R2 or S3).

## Decision

**Option B: Python with FastAPI on PostgreSQL, in its own repository** (separate from this frontend repository). Decided by the project owner on 2026-11-01. A monorepo (npm workspaces with a shared contract package) was considered and rejected because the backend is not TypeScript; the two repositories meet only at the OpenAPI contract.

Working choices that follow from it (refined in B0.2 to B0.5; change them with a new ADR if the team disagrees):

- FastAPI with Pydantic v2 for validation and OpenAPI generation; SQLAlchemy 2.x with Alembic migrations; `uv` for dependencies; pytest against a real PostgreSQL; Ruff and a type checker in CI.
- Row locking with `SELECT ... FOR UPDATE` (`with_for_update()`) inside transactions, as the spec requires for the donation cap.
- Paystack in test mode (spec D3) and a scheduled job for reservation expiry.
- Authentication is written by hand, with no external auth service: [ADR-011](./ADR-011-authentication.md).
- Hosting starts on Railway (API and PostgreSQL), moving to a VPS later: [ADR-012](./ADR-012-hosting-railway.md).
- Files are stored in MinIO behind an S3-compatible adapter: [ADR-013](./ADR-013-object-storage-minio.md).

## Rationale

- FastAPI generates an OpenAPI 3.1 document from the code, which is the contract the frontend depends on (ADR-003, B0.3). Pydantic gives strict request and response validation.
- `select_for_update()` is first class, so the cap (spec 4.2) is enforced in the database transaction.
- A separate repository keeps each toolchain simple (npm here, `uv` there), lets each deploy independently (Vercel for the frontend) and avoids forcing Python into an npm workspace.

## Consequences

- B0.1 is done. B0.2 to B0.5 start in the backend repository, `haneefojay/amanah-api`.
- The frontend loses the option of importing the Zod schemas from a shared package. `src/lib/api/schemas.ts` stays as the frontend's copy of the contract and is reconciled with the generated OpenAPI document (F0.4, B0.3), for example by generating TypeScript types from it.
- The MSW mock API stays until each endpoint is integrated (ADR-003).
- Two repositories to keep in step: contract changes are announced in the matching `F` and `B` items.
- The team works in two languages. Local setup must stay cross-platform for Windows (`uv`, Docker Compose for PostgreSQL).
