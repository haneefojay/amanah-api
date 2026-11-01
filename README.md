# Amanah API

The backend service for [Amanah](./PROJECT.md), a transparent Islamic donation platform. FastAPI, PostgreSQL, MinIO.

The frontend lives in [haneefojay/amanah](https://github.com/haneefojay/amanah).

## Status

**Documentation only.** The service skeleton is roadmap item **B0.2**. Until it lands there is nothing to install or run. Read [`PROJECT.md`](./PROJECT.md), then [`docs/roadmap/ROADMAP_INDEX.md`](docs/roadmap/ROADMAP_INDEX.md).

## Planned local setup (to be confirmed by B0.2 and B0.4)

Prerequisites: Python 3.12 or newer, [`uv`](https://docs.astral.sh/uv/), Docker Desktop (for PostgreSQL and MinIO), Git. It must work on Windows, macOS and Linux.

```bash
cp .env.example .env              # on Windows PowerShell: copy .env.example .env
docker compose up -d              # PostgreSQL and MinIO
uv sync
uv run alembic upgrade head
uv run fastapi dev                # http://localhost:8000, docs at /api/docs
uv run pytest                     # tests against a real PostgreSQL
```

Command names above are the intended conventions; the item that creates each one updates this file.

## Documentation

| File                      | Purpose                                                  |
| ------------------------- | -------------------------------------------------------- |
| `docs/amanah-mvp-spec.md` | Product specification                                    |
| `docs/roadmap/`           | Backend roadmap (B0 to B12) and the status index         |
| `docs/decisions/`         | Architecture Decision Records                            |
| `docs/architecture.md`    | Architecture, contract, auth, storage, deployment        |
| `AGENTS.md` / `CLAUDE.md` | Guides for AI agents and contributors                    |
| `CHANGELOG.md`            | Change history                                           |
