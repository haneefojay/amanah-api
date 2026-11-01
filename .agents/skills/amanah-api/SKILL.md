---
name: amanah-api
description: Project rules for the Amanah API, the backend of the transparent Islamic donation platform (FastAPI, PostgreSQL). Use for ANY work in this repository — endpoints, the donation cap and reservations, payments and webhooks, auth, storage, migrations, tests, roadmap items, ADRs, changelog or commits — and whenever money, donations, campaigns, evidence, witnesses or the audit log are involved.
---

# Amanah API project skill

Amanah lets verified Islamic organisations publish itemised needs with a fixed target. Donors give, and follow every naira through a public accountability page. **The product's whole value is trust.** A wrong number, a donation that overshoots the target, or a silent failure is worse than a missing feature. The backend is where those guarantees are enforced.

Deadline for the challenge: **1 November 2026**; the project continues as a real product. When in doubt, cut scope, not quality.

## Before you start

1. Read `PROJECT_MEMORY.md`, then `docs/roadmap/ROADMAP_INDEX.md` (current focus and status).
2. Find the roadmap item (`B<n>.<m>`) the work belongs to and read its full entry in `docs/roadmap/BACKEND_ROADMAP.md`: scope, tests, Definition of Done, and the frontend items it unblocks.
3. Read the spec sections it cites in `docs/amanah-mvp-spec.md` and the related ADRs.
4. If no roadmap item covers the work, say so and propose one before building.

| Task | Read |
| ---- | ---- |
| Money, donations, campaign status, roles, evidence, witnesses, privacy | [references/domain-rules.md](references/domain-rules.md) |
| Claiming or finishing a roadmap item, ADRs, changelog, commits, PRs | [references/workflow.md](references/workflow.md) |
| How the pieces fit | `docs/architecture.md` |

## Hard rules (never break these)

1. **Money is integer kobo.** `BIGINT` columns, Pydantic `int`. No `float`, no `Decimal`.
2. **The cap is enforced in the database transaction** with `SELECT … FOR UPDATE` (`with_for_update()`), never only in memory. Prove it with the concurrency suite (B6.3).
3. **Webhooks:** verify the signature, then call the provider's verify endpoint; idempotent through a unique `provider_reference`.
4. **Append-only audit log** for every state change.
5. **Access control** on every non-public route: role guard plus organisation scoping. A test lists routes and fails if one is unguarded.
6. **Auth is hand-written** (ADR-011): argon2id, server-side sessions, httpOnly cookie, CSRF protection. No JWT in `localStorage`, no external auth service.
7. **Secrets only in environment variables.** New config goes in `.env.example`.
8. **Public responses never include donor email or phone.**
9. **General donations only.** Zakat and waqf never appear anywhere.
10. **Integration tests run against a real PostgreSQL.** Nothing is done without the tests listed in its roadmap item.
11. **The contract is OpenAPI.** Keep it current and tell the user which frontend items must follow (`src/lib/api/schemas.ts`, MSW handlers in https://github.com/haneefojay/amanah).
12. **No AI attribution** in commits or PRs (no `Co-Authored-By` AI trailers, no "Generated with" lines).
13. **Stop and ask** before touching an open decision (spec §11 D1–D11), adding a runtime dependency not covered by an ADR, or doing anything hard to reverse.

## Finish line

Lint, types and tests pass · OpenAPI regenerated if endpoints changed · roadmap index updated (and the frontend mirror noted) · `CHANGELOG.md` entry · ADR for any lasting decision · summary to the user with what was tested and what needs their decision.
