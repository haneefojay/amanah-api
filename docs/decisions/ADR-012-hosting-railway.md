# ADR-012: Backend hosting on Railway, moving to a VPS later

- **Status:** Accepted
- **Date:** 2026-11-01
- **Deciders:** Project owner (Haneef)
- **Related:** BACKEND_ROADMAP B0.4, B12.4; ADR-004; ADR-008 (frontend on Vercel); ADR-013

## Context

The API, PostgreSQL and object storage need a home. The owner wants the fastest route to a working deployment now, and expects to move to a VPS as the project grows. These hosting choices may change.

## Options considered

### Option A: Railway for the API, PostgreSQL and MinIO

- Pros: quick to set up from a Dockerfile; managed PostgreSQL in the same project; environment variables and deploys from GitHub; private networking between services.
- Cons: a platform dependency; costs grow with usage; backup and retention settings must be checked and tested rather than assumed.

### Option B: A VPS from the start (Docker Compose behind a reverse proxy)

- Pros: full control and predictable cost.
- Cons: we run the server, TLS, backups and patching ourselves, which is slower to set up.

### Option C: Render, Fly.io or another PaaS

- Pros: similar speed to Railway.
- Cons: no advantage over Railway for this project.

## Decision

Option A to start, with a planned move to Option B. Staging and production are separate Railway environments, each with its own PostgreSQL and MinIO service.

To keep the move cheap:

- The API ships as a **Dockerfile** and reads all configuration from environment variables (twelve-factor). No Railway-specific code.
- A `docker-compose.yml` in this repository runs the API, PostgreSQL and MinIO locally, and is the starting point for a VPS.
- Migrations run on deploy (B12.4), and secrets live only in the platform's environment variables.
- Backups of PostgreSQL are configured and a restore is tested before launch (B12.4).

## Rationale

Railway gets a real deployment running fastest, and the Docker-first rule keeps the VPS option open.

## Consequences

- Positive: quick staging URL for `/health` (B0 Definition of Done); simple environment management.
- Negative or risks: platform lock-in is limited to deployment config; the frontend origin and API origin must be arranged for cookies (ADR-011); MinIO needs a persistent volume and a public endpoint for signed URLs (ADR-013).
- Follow-up: B12.4, B12.3, B0.2 (Dockerfile), B0.4 (Compose), and frontend F0.6 (`NEXT_PUBLIC_API_BASE_URL`).
