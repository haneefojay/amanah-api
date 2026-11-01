# Changelog

All notable changes to the Amanah API are recorded here. This file is the project's running memory: every change by any agent or contributor gets an entry.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Dates are in Africa/Lagos time. Reference roadmap IDs (`B6.1`) and ADRs where relevant.

Sections per release: **Added**, **Changed**, **Fixed**, **Removed**, **Security**, **Decisions**, **Docs**.

## [Unreleased]

### Added

- **Service skeleton (B0.2):** FastAPI app factory (`app/main.py`), `GET /health` that checks the database (503 when it is down), settings loaded with pydantic-settings that fail fast on a missing `DATABASE_URL`, structured logging (JSON in staging and production), a request ID on every response, CORS restricted to the configured frontend origins with credentials, the standard error envelope for HTTP, validation and unhandled errors (no stack traces to clients), docs at `/api/docs`. A `Dockerfile` for Railway or any Docker host.
- **Database layer (B0.4):** async SQLAlchemy 2 with asyncpg, an Alembic baseline migration, `docker-compose.yml` for PostgreSQL 16 (with a separate `amanah_test` database) and MinIO.
- **Test harness (B0.5):** pytest and pytest-asyncio against a real PostgreSQL. Each test gets a session in a rolled-back transaction, and an HTTP client for the app. 19 tests cover config, `/health`, request IDs, CORS, the error envelope, rollback isolation, and that migrations apply, roll back and apply again.
- **API contract (B0.3):** Pydantic models for every request and response (`app/schemas/`), all 28 spec routes as `501 NOT_IMPLEMENTED` stubs tied to their roadmap item (`x-roadmap`), the session-cookie security scheme on organisation, witness and admin routes, an error-code catalogue published as `info.x-error-codes`, and the generated `openapi.json` (`scripts/export_openapi.py`, with `--check`). Tests fail if the file is stale, and validate the frontend mock payloads against the models.
- **CI:** GitHub Actions run Ruff, mypy (strict), migrations and pytest against a PostgreSQL service, plus a Docker build.

### Changed

- **Modular monolith (B0.6, ADR-015):** the layered `app/api/` and `app/schemas/` packages become `app/modules/{auth, organisations, campaigns, donations, accountability, audit, admin}`, each with `router.py`, `schemas.py`, `models.py`, `service.py` and a public interface in `__init__.py`. Shared pieces move to `app/core` (`schemas.py`, `security.py`, `stubs.py`); `GET /health` moves to `app/health.py`; `app/main.py` wires the module routers. `openapi.json` is unchanged (byte-identical, all 28 routes). A new test, `tests/architecture/test_module_boundaries.py`, fails the build when a module imports another module's internals, when modules form a cycle, or when `core` or `db` import upward.
- **Python 3.14 and FastAPI 0.162** (owner decision, 2026-11-01): `.python-version`, the Dockerfile, `requires-python`, Ruff and mypy targets move from 3.12 to 3.14; the FastAPI floor is now 0.162.

### Decisions

- **ADR-004 accepted:** FastAPI on PostgreSQL (SQLAlchemy, Alembic, pytest), in this separate repository.
- **ADR-011:** authentication is written by hand: argon2id passwords and server-side sessions in PostgreSQL, httpOnly cookie, CSRF protection; no external auth service.
- **ADR-012:** hosting starts on Railway (API and PostgreSQL) and moves to a VPS later; Dockerfile and environment-variable configuration keep it portable.
- **ADR-013:** files are stored in MinIO behind an S3-compatible adapter.
- **ADR-015:** the API is a modular monolith with import boundaries enforced by a test.

### Docs

- `docs/api-contract.md` describes the contract conventions.
- Repository created with the project overview, `AGENTS.md`, `CLAUDE.md`, the MVP specification, the backend roadmap (B0 to B12) refined with the chosen tools, the roadmap index (B0.1 done), ADR-003, ADR-004 and ADR-011 to ADR-013, an architecture note, the `amanah-api` Claude skill and the `/phase` command.
