# Architecture Decision Records

Every significant decision about Amanah (technology, architecture, process, or how a spec open decision was resolved) is recorded as an ADR. ADRs are **append-only history**: never rewrite an accepted ADR. To change a decision, write a new ADR that supersedes the old one and mark the old one `Superseded by ADR-XXX`.

ADR numbering is **shared across the frontend and backend repositories**. This repository holds the backend decisions; the frontend decisions are in https://github.com/haneefojay/amanah/tree/main/docs/decisions. The next free number is **ADR-016** (ADR-014 is taken in the frontend repository) (check the frontend repository's index too before taking one).

## Index

| ADR | Title | Status | Date |
| --- | ----- | ------ | ---- |
| [ADR-003](./ADR-003-frontend-backend-separation.md) | Separate backend service and contract-first frontend development | Accepted | 2026-10-18 |
| [ADR-004](./ADR-004-backend-stack.md) | Backend technology stack: FastAPI on PostgreSQL, separate repository | Accepted | 2026-11-01 |
| [ADR-011](./ADR-011-authentication.md) | Hand-written authentication with server-side sessions | Accepted | 2026-11-01 |
| [ADR-012](./ADR-012-hosting-railway.md) | Backend hosting on Railway, moving to a VPS later | Accepted | 2026-11-01 |
| [ADR-013](./ADR-013-object-storage-minio.md) | Object storage on MinIO behind an S3-compatible adapter | Accepted | 2026-11-01 |
| [ADR-015](./ADR-015-modular-monolith.md) | Modular monolith with enforced module boundaries | Accepted | 2026-11-01 |

Frontend ADRs (for reference): ADR-001 framework, ADR-002 PWA strategy, ADR-005 testing, ADR-006 libraries, ADR-007 typography, ADR-008 hosting on Vercel, ADR-009 shadcn/ui, ADR-010 public accountability data, ADR-014 no mock API.

## How to add an ADR

1. Copy [`TEMPLATE.md`](./TEMPLATE.md) to `ADR-XXX-short-kebab-title.md` with the next number (three digits, never reused).
2. Fill in every section. **Options considered** must list at least two real options with pros and cons.
3. Set the status to `Proposed` while it awaits the owner, or `Accepted` once decided. Always include the date.
4. Add a row to the index above and an entry to `CHANGELOG.md`. If the other repository is affected, add a row to its index too.
5. If the decision changes roadmap scope, update `docs/roadmap/ROADMAP_INDEX.md`.

## Status values

`Proposed`, `Accepted`, `Rejected`, `Deprecated`, or `Superseded by ADR-XXX`.
