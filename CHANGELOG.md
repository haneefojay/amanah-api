# Changelog

All notable changes to the Amanah API are recorded here. This file is the project's running memory: every change by any agent or contributor gets an entry.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Dates are in Africa/Lagos time. Reference roadmap IDs (`B6.1`) and ADRs where relevant.

Sections per release: **Added**, **Changed**, **Fixed**, **Removed**, **Security**, **Decisions**, **Docs**.

## [Unreleased]

### Decisions

- **ADR-004 accepted:** FastAPI on PostgreSQL (SQLAlchemy, Alembic, pytest), in this separate repository.
- **ADR-011:** authentication is written by hand: argon2id passwords and server-side sessions in PostgreSQL, httpOnly cookie, CSRF protection; no external auth service.
- **ADR-012:** hosting starts on Railway (API and PostgreSQL) and moves to a VPS later; Dockerfile and environment-variable configuration keep it portable.
- **ADR-013:** files are stored in MinIO behind an S3-compatible adapter.

### Docs

- Repository created with the project overview, `AGENTS.md`, `CLAUDE.md`, the MVP specification, the backend roadmap (B0 to B12) refined with the chosen tools, the roadmap index (B0.1 done), ADR-003, ADR-004 and ADR-011 to ADR-013, an architecture note, the `amanah-api` Claude skill and the `/phase` command.
