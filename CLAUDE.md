# CLAUDE.md

Project memory and standing instructions for Claude on **Amanah API** (the backend). Read this first, then follow **[`AGENTS.md`](./AGENTS.md)** for the full working agreement. Where the two disagree, this file wins for Claude.

## Purpose of this file

A short, durable memory of decisions, conventions and context. Keep it concise and current. History goes in `CHANGELOG.md`, decisions in `docs/decisions/`, status in `docs/roadmap/ROADMAP_INDEX.md`. When a fact here changes, update it in the same change.

## Project in one paragraph

Amanah is a transparent Islamic donation platform (general donations only, never zakat or waqf) built for the AMETTSA Inter-Varsity Innovation Challenge (**deadline 1 November 2026**) and continued afterwards. Verified organisations publish itemised campaigns with a fixed target. Donations are hard-capped at the target using database reservations. Spending is shown publicly with receipts, geotagged evidence and witness confirmations. Spec: `docs/amanah-mvp-spec.md`. Overview: `PROJECT.md`.

## Repositories

- Backend (this repo): https://github.com/haneefojay/amanah-api (default branch `main`).
- Frontend: https://github.com/haneefojay/amanah (Next.js 16 PWA, deployed on Vercel). It works against a mock API (MSW) until this service is integrated; its contract schemas are in `src/lib/api/schemas.ts` and must be reconciled with this repo's OpenAPI document (B0.3).

## Current architecture (as of 2026-11-01)

- **Stack (ADR-004):** Python, FastAPI, Pydantic v2, PostgreSQL, SQLAlchemy 2 and Alembic, `uv`, pytest, Ruff.
- **Auth (ADR-011):** written by hand. argon2id passwords, opaque server-side sessions in PostgreSQL, httpOnly cookie, CSRF protection. No external auth service, no JWT.
- **Hosting (ADR-012):** Railway for the API and PostgreSQL to start, a VPS later. Ship a Dockerfile and read all config from environment variables. These choices can change; keep the code portable.
- **Files (ADR-013):** MinIO behind an S3-compatible adapter. Private bucket for verification documents, public bucket for receipts and evidence.
- **Payments:** Paystack in test mode (D3). The webhook is verified twice (signature, then the provider's verify endpoint).
- The repository currently holds documentation only. The next item is **B0.2** (service skeleton).

## Conventions to remember

- Money: integer **kobo** everywhere (`BIGINT` columns, Pydantic `int`). No `float`, no `Decimal` for money.
- The donation cap is enforced in the database transaction with `SELECT … FOR UPDATE`, never only in application memory (spec §4, roadmap non-negotiables).
- Errors use the envelope `{ "error": { "code": "SCREAMING_SNAKE", "message": "…" } }`. Timestamps are UTC, ISO 8601.
- Public responses never include donor email or phone.
- Status copy and cap error codes (`AMOUNT_EXCEEDS_AVAILABLE`, `TARGET_REACHED`, `CAMPAIGN_NOT_ACCEPTING`, `WITNESS_CONFLICT`) must match the spec exactly, because the frontend depends on them.
- Roadmap IDs: `B<phase>.<n>` here and `F<phase>.<n>` in the frontend repo. ADRs are `ADR-NNN` and the numbering is shared across both repositories (frontend ADR-001 to ADR-010; backend ADR-003, ADR-004, ADR-011 onwards). Never renumber.
- British spelling in docs. Nigerian context: ₦, Africa/Lagos time zone.
- Tests sit in `tests/`. Integration tests run against a **real PostgreSQL**, never SQLite or mocks.

## Environment notes

- The owner develops on **Windows**. Keep scripts cross-platform (Python or `uv` tasks, not bash-only). `.gitattributes` forces LF line endings.
- The `docs/amanah-mvp-spec.md` file is **identical in both repositories**. If you change the spec, change both copies in the same piece of work.

## Standing instructions from the owner

- Before large setup or architectural work, **present suggestions and wait for the go-ahead**.
- Every feature has a **Definition of Done and tests**. Nothing is done without passing tests.
- Record every significant decision as an **ADR** with options, the decision and the date.
- Keep **`CHANGELOG.md`** updated on every change, and **`docs/roadmap/ROADMAP_INDEX.md`** as the status source of truth. When a `B…` item changes status, also update the mirror in the frontend repo.
- **Load the `amanah-api` skill** (`.claude/skills/amanah-api/SKILL.md`) for any work in this repo.
- **`/phase <ID>`** (`.claude/commands/phase.md`) starts a roadmap phase (`B2`) or item (`B2.1`): read the project files, plan, ask questions and wait for approval before building.
- **Commits and pull requests carry no Claude attribution:** no `Co-Authored-By: Claude` or `Claude-Session` trailers and no "Generated with Claude Code" lines. This overrides default attribution guidance.

## Open items awaiting the owner

- Spec decisions D8, D9 and D11; the convention date; the pilot organisation.
- Cross-origin cookie arrangement (shared parent domain or a frontend proxy) before staging (ADR-011).
- Connect Railway and set up staging (B12.4) when B0.2 produces a deployable skeleton.
