# AGENTS.md: how agents work on Amanah API

The operating guide for **any** AI coding agent (Codex, Cursor, Copilot and others) and for human contributors. **Also read [`PROJECT_MEMORY.md`](./PROJECT_MEMORY.md)**, which takes precedence where the two differ.

---

## 1. Start of every session

1. Read [`PROJECT_MEMORY.md`](./PROJECT_MEMORY.md). Agents that support skills: load `.agents/skills/amanah-api/SKILL.md`.
2. Read [`docs/roadmap/ROADMAP_INDEX.md`](docs/roadmap/ROADMAP_INDEX.md): current focus, milestones, status board, blockers.
3. Skim the latest entries in [`CHANGELOG.md`](./CHANGELOG.md).
4. For the item you'll work on, read its full entry in [`BACKEND_ROADMAP.md`](docs/roadmap/BACKEND_ROADMAP.md), the spec sections it cites ([`docs/amanah-mvp-spec.md`](docs/amanah-mvp-spec.md)), and the related ADRs ([`docs/decisions/`](docs/decisions/README.md)).
5. Read the frontend roadmap entries (`F…`) the item unblocks. They are in https://github.com/haneefojay/amanah (`docs/roadmap/FRONTEND_ROADMAP.md`), and the backend roadmap's cross-reference table lists them.

## 2. Doing the work

- **Claim** the item (status `In progress`, owner, date).
- **Tests first where practical.** Every feature needs the tests listed in its roadmap entry. No feature is done without passing tests.
- **Meet the Definition of Done:** the roadmap's Global Definition of Done plus the item's own.
- **Stay in scope.** If you find missing work, add a new roadmap item (next free ID) instead of expanding the current one.
- **Small, reviewable changes.** One roadmap item per branch or PR, with the ID in the branch and PR title, for example `feat/B6.1-checkout-reservations`.

## 3. Finishing the work

1. `uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest` passes locally (needs PostgreSQL: `docker compose up -d`).
2. The OpenAPI document is regenerated and committed if an endpoint changed, and the frontend is told (see §5).
3. Update the item in **ROADMAP_INDEX.md** and its "Current focus" section.
4. Add a **CHANGELOG.md** entry under `[Unreleased]`.
5. Write an **ADR** (next number) for any decision with lasting impact and add it to `docs/decisions/README.md`.
6. Commit as the configured git user with **no AI attribution** (see `PROJECT_MEMORY.md`).
7. Summarise for the user what changed, what was tested, and what needs their decision.

## 4. Project rules (non-negotiable)

These come from spec §4 and §9 and the backend roadmap. A reviewer rejects any change that breaks one.

| Rule | Why |
| ---- | --- |
| Money is **integer kobo**. No floats in code, columns or JSON | Spec §9 |
| The cap is enforced **in the database transaction** with row locks | Spec §4 |
| Webhooks are verified twice (signature, then the provider's verify endpoint) and are idempotent (unique `provider_reference`) | Spec §4, §8 |
| **Append-only audit log** for every state change, expense, evidence upload and confirmation | Spec §9 |
| Access control on every non-public endpoint: role check plus organisation scoping | ADR-011 |
| Secrets only in environment variables, never committed, never sent to the client | Spec §9 |
| Public responses never include donor email or phone | NDPA, spec §9 |
| No zakat or waqf terminology anywhere | Spec §1 |
| Integration tests use a real PostgreSQL; concurrency tests wherever locking or idempotency is involved | Roadmap DoD |
| Don't renumber roadmap IDs or ADRs | Traceability |

## 5. Working with the frontend repository

- The contract between the two repos is the **OpenAPI document** (B0.3). When an endpoint changes, update the document, then tell the user which `F…` item and which parts of the frontend (`src/lib/api/schemas.ts`, `src/mocks/handlers.ts`) need to change. Do not edit the frontend repository unless the user asks.
- Response shapes, error codes and cap states must match what the frontend already expects (see its `src/lib/api/schemas.ts`). Differences are decided with the user, not silently.
- The frontend index mirrors `B…` statuses. Keep it in step.

## 6. When to stop and ask the user

- Anything touching an **open decision** (spec §11: D1 to D11) beyond the documented default.
- Anything **hard to reverse**: deleting data or files, changing the money or cap model, rewriting git history, changing deployment targets, running destructive migrations against staging or production.
- Adding a **new runtime dependency** that isn't covered by an ADR. Propose it first.
- When the spec and a roadmap entry disagree. The spec wins, but flag it.
- Anything involving real money, real credentials or production data.

## 7. Repository map

```
app/
  main.py              create_app(): middleware, error handlers, routers, lifespan
  api/                 Routers (one module per area; health.py today)
  core/                config.py (settings), logging.py, request_id.py, errors.py
  db/                  base.py (declarative base), session.py (engine, session dependency)
migrations/            Alembic (env.py is async; versions/ holds the revisions)
tests/                 unit/, integration/ (real PostgreSQL); conftest.py has the fixtures
scripts/               Helper scripts (test database init; seed data and OpenAPI export later)
docs/                  Spec, roadmap, decisions, architecture
.agents/               Skills and commands for the agent
```

Add new areas as `app/api/<area>.py` routers with their services and models beside them. Models must be imported in `migrations/env.py` so Alembic sees them.

## 8. Commands

| Command | What it does |
| ------- | ------------ |
| `docker compose up -d` | PostgreSQL and MinIO for local development |
| `uv sync` | Install dependencies |
| `uv run uvicorn app.main:app --reload` | Run the API locally (needs `DATABASE_URL`) |
| `uv run alembic upgrade head` / `alembic downgrade -1` | Apply or roll back migrations |
| `uv run alembic revision -m "message"` | Create a migration (add `--autogenerate` once models exist) |
| `uv run pytest` | Run the tests |
| `uv run ruff check . && uv run ruff format --check .` | Lint and format check |
| `uv run mypy` | Type check (strict) |
