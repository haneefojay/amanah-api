# AGENTS.md: how agents work on Amanah API

The operating guide for **any** AI coding agent (Claude, Codex, Cursor, Copilot and others) and for human contributors. **Claude: also read [`CLAUDE.md`](./CLAUDE.md)**, which takes precedence where the two differ.

---

## 1. Start of every session

1. Read [`CLAUDE.md`](./CLAUDE.md). Agents that support skills: load `.claude/skills/amanah-api/SKILL.md`.
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

1. Lint, type check and tests pass locally (the exact commands are added by B0.2; until then, none apply).
2. The OpenAPI document is regenerated and committed if an endpoint changed, and the frontend is told (see §5).
3. Update the item in **ROADMAP_INDEX.md** and its "Current focus" section.
4. Add a **CHANGELOG.md** entry under `[Unreleased]`.
5. Write an **ADR** (next number) for any decision with lasting impact and add it to `docs/decisions/README.md`.
6. Commit as the configured git user with **no AI attribution** (see `CLAUDE.md`).
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

## 7. Repository map (target layout; B0.2 creates it)

```
app/                   FastAPI application (routers, services, models, schemas, core config)
migrations/            Alembic migrations
tests/                 unit/, integration/ (real PostgreSQL), concurrency/
scripts/               Seed data, OpenAPI export, helpers
docs/                  Spec, roadmap, decisions, architecture
.claude/               Skills and commands for Claude
```

The layout may change when B0.2 is designed; update this section then.

## 8. Commands (target; B0.2 and B0.4 add them)

| Command | What it does |
| ------- | ------------ |
| `docker compose up -d` | PostgreSQL and MinIO for local development |
| `uv sync` | Install dependencies |
| `uv run fastapi dev` | Run the API locally |
| `uv run alembic upgrade head` | Apply migrations |
| `uv run pytest` | Run the tests |
| `uv run ruff check . && uv run ruff format --check .` | Lint and format check |
