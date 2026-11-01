# Amanah API

The backend service for [Amanah](./PROJECT.md), a transparent Islamic donation platform. FastAPI, PostgreSQL, MinIO.

The frontend lives in [haneefojay/amanah](https://github.com/haneefojay/amanah).

## Status

The service skeleton runs: `GET /health` (checks the database), the standard error envelope, request IDs, CORS, Alembic migrations and a pytest harness against a real PostgreSQL. There is no business logic yet. Read [`PROJECT.md`](./PROJECT.md), then [`docs/roadmap/ROADMAP_INDEX.md`](docs/roadmap/ROADMAP_INDEX.md).

## Local setup

Prerequisites: [`uv`](https://docs.astral.sh/uv/) (it installs Python 3.14 for you), Docker Desktop (for PostgreSQL and MinIO), Git. The commands are cross-platform; the Windows PowerShell form is shown where it differs.

```bash
cp .env.example .env              # on Windows PowerShell: copy .env.example .env
docker compose up -d              # PostgreSQL and MinIO
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload   # http://localhost:8000, docs at /api/docs
uv run pytest                     # tests against a real PostgreSQL
```

Load `.env` first or export `DATABASE_URL` (the app also reads `.env` itself). Tests use `TEST_DATABASE_URL`, which defaults to the `amanah_test` database that `docker compose` creates.

### Checks (the same ones CI runs)

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run pytest
```

## Documentation

| File                      | Purpose                                                  |
| ------------------------- | -------------------------------------------------------- |
| `docs/amanah-mvp-spec.md` | Product specification                                    |
| `docs/roadmap/`           | Backend roadmap (B0 to B12) and the status index         |
| `docs/decisions/`         | Architecture Decision Records                            |
| `docs/architecture.md`    | Architecture, contract, auth, storage, deployment        |
| `AGENTS.md` / `PROJECT_MEMORY.md` | Guides for AI agents and contributors                    |
| `CHANGELOG.md`            | Change history                                           |
