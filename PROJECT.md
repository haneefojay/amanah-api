# Amanah API

> **Amanah** (أمانة) means trust: the obligation to safeguard what is placed in one's care.

Amanah is a transparent Islamic donation platform. Verified Islamic organisations (mosques, orphanages, Islamic societies, community groups) publish specific, itemised needs. Donors give to those needs and follow exactly how the money is spent through a live accountability page: receipts, photos, and independent witness confirmation.

**This repository is the backend API service.** The frontend is a separate repository: [haneefojay/amanah](https://github.com/haneefojay/amanah) (Next.js PWA).

## Why

Entry for the **AMETTSA Inter-Varsity Innovation Challenge** (AMETTSA 5.0 Annual Convention, Summit University, Offa, Kwara State). Submission deadline: **1 November 2026**. The project continues beyond the challenge as a properly built product.

## What makes it different (and what the backend must guarantee)

1. **The system enforces the donation cap, not just a policy.** An organisation can never receive more than its stated target. The backend does this with database reservations and row locks (spec §4). The frontend only reflects it.
2. **Accountability is public by default.** Target, raised, spent, receipts, geotagged evidence and witness confirmations are served by public endpoints that never expose donor contact data.
3. **Independent witnesses** confirm or dispute delivery. A witness cannot be an admin of the organisation.
4. **Append-only audit log** for every state change.

## Hard boundaries

- **General donations only.** Zakat and waqf are permanently out of scope and must not appear in code, data, messages or docs.
- **Test-mode payments only** for the MVP (Paystack test mode).
- **When in doubt, cut scope.**

## Users and roles

| Role               | Does                                                                            |
| ------------------ | ------------------------------------------------------------------------------- |
| Donor (guest)      | Browses, donates, follows accountability                                        |
| `ORG_ADMIN`        | Creates campaigns, logs expenses and evidence, posts updates, assigns witnesses |
| `WITNESS`          | Confirms or disputes delivery per item                                          |
| `PLATFORM_ADMIN`   | Verifies organisations, reviews campaigns, resolves excess, audits              |

## Architecture at a glance

See [`docs/architecture.md`](docs/architecture.md).

```
┌──────────────────────────────┐   HTTPS / JSON + cookie   ┌───────────────────────────────┐
│  Frontend (haneefojay/amanah)│  ───────────────────────► │  This repository: API         │
│  Next.js 16 PWA on Vercel    │  ◄─────────────────────── │  FastAPI · PostgreSQL · MinIO │
└──────────────────────────────┘                           │  Paystack (test mode)         │
                                                           └───────────────────────────────┘
```

## Stack and decisions

| Concern        | Choice                                                    | ADR                                                  |
| -------------- | --------------------------------------------------------- | ---------------------------------------------------- |
| Language/API   | Python, FastAPI, Pydantic v2                              | [ADR-004](docs/decisions/ADR-004-backend-stack.md)   |
| Database       | PostgreSQL, SQLAlchemy 2, Alembic                         | ADR-004                                              |
| Authentication | Hand-written: argon2id and server-side sessions           | [ADR-011](docs/decisions/ADR-011-authentication.md)  |
| Hosting        | Railway (API and PostgreSQL) now, a VPS later             | [ADR-012](docs/decisions/ADR-012-hosting-railway.md) |
| File storage   | MinIO behind an S3-compatible adapter                     | [ADR-013](docs/decisions/ADR-013-object-storage-minio.md) |
| Payments       | Paystack, test mode (spec D3)                             | spec §8                                              |

## Repositories

| Part                  | Repository                                   |
| --------------------- | -------------------------------------------- |
| Backend (this repo)   | https://github.com/haneefojay/amanah-api     |
| Frontend              | https://github.com/haneefojay/amanah         |

## Where things live

| Path                          | Purpose                                                               |
| ----------------------------- | --------------------------------------------------------------------- |
| `docs/amanah-mvp-spec.md`     | The product specification (source of truth for requirements)          |
| `docs/roadmap/`               | Backend roadmap and **ROADMAP_INDEX.md** (status)                     |
| `docs/decisions/`             | Architecture Decision Records                                         |
| `docs/architecture.md`        | How the pieces fit together; contract, auth, storage, deployment      |
| `AGENTS.md` / `PROJECT_MEMORY.md`     | How any AI agent or contributor works here / the agent's project memory  |
| `CHANGELOG.md`                | Every notable change                                                  |
| `.agents/skills/amanah-api/`  | Project skill for the agent                                              |

## Status

See [`docs/roadmap/ROADMAP_INDEX.md`](docs/roadmap/ROADMAP_INDEX.md). No application code exists yet: the next step is B0.2 (service skeleton).
