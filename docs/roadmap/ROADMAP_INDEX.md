# Roadmap Index (backend)

**This is the single source of truth for backend (`B…`) roadmap status.** The frontend repository ([haneefojay/amanah](https://github.com/haneefojay/amanah)) keeps its own index for `F…` items and a mirror of the `B…` rows; when a `B…` status changes here, update that mirror in the same piece of work.

| File | Contents |
| --- | --- |
| [BACKEND_ROADMAP.md](./BACKEND_ROADMAP.md) | Phases `B0` to `B12`: scope, tests and Definition of Done |
| [../amanah-mvp-spec.md](../amanah-mvp-spec.md) | The product specification |
| [Frontend roadmap](https://github.com/haneefojay/amanah/blob/main/docs/roadmap/FRONTEND_ROADMAP.md) | Phases `F0` to `F13` (other repository) |

**Last updated:** 1 November 2026.

---

## 1. How to use the roadmap (agent workflow)

1. **Orient.** Read `CLAUDE.md` and `AGENTS.md`, then sections 2 (Current focus) and 4 (Status board) here.
2. **Pick work.** Take the highest-priority `Not started` item whose dependencies are `Done`. Prefer P0 over P1 over P2, items in the current milestone, and items that unblock the most P0 frontend work (see the cross-reference table at the end of the backend roadmap). Never start a `Blocked` item.
3. **Claim it.** Set `In progress`, put your name or agent ID in **Owner**, and set **Updated** to today.
4. **Read the full entry** in `BACKEND_ROADMAP.md`, and the spec sections it cites.
5. **Build test-first where practical.** Meet the Global Definition of Done plus the item's own.
6. **Finish.** Set `Done`, add the PR link in **Notes**, add a `CHANGELOG.md` entry, update section 2, and tell the frontend side (its mirror and the matching `F` item).
7. **When blocked:** set `Blocked`, write the reason in Notes, add it to section 5 and tell the user.
8. **When a decision is needed:** write an ADR with status `Proposed` and ask the user.
9. **Scope changes:** never renumber. New items take the next free ID; removed items are marked `Dropped` with a reason.

Status values: `Not started`, `In progress`, `Done`, `Blocked`, `Dropped`.

---

## 2. Current focus

- **Now:** B0 is done (B0.1 to B0.5): service skeleton, database layer, test harness, and the OpenAPI contract (`openapi.json`, 28 stub routes). Python 3.14, FastAPI 0.162. Auth, hosting and file storage are decided (ADR-011 to ADR-013).
- **Next:** restructure as a modular monolith (ADR-015, own thread), then B1 (schema, audit log, seed data) and B2 (auth). The frontend generates types from `openapi.json` in parallel. Staging on Railway (B12.4) can start now that CI is green.
- **Decisions needed from the team:** spec open decisions D8, D9 and D11, the convention date, and the pilot organisation.

---

## 3. Milestones (deadline 1 November 2026)

| Milestone                   | Target date | Exit criteria                                                                                                      |
| --------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------ |
| **M0: Foundation**          | 18 Oct      | F0.1 to F0.5 done (F0.5 once the repository is on GitHub)                                                          |
| **M1: Backbone**            | 22 Oct      | ADR-004 accepted; B0 and B1 done; F1 done; F2.1 to F2.3 and F3.1 to F3.5 `Done (mocked)`                           |
| **M2: Money flow**          | 26 Oct      | B2, B4.1 to B4.3, B5, B6 and B7.1 to B7.3 and B7.5 done; F4 and F5 done (integrated); concurrency suite B6.3 green |
| **M3: Accountability loop** | 29 Oct      | B3, B8, B9 and B10.1 to B10.2 done; F6 to F11 P0 items done; F3 integrated                                         |
| **M4: Demo ready**          | 31 Oct      | F12.3, F13.3, F13.4 and B12 P0 done; demo rehearsed twice on a real phone                                          |
| **Submission**              | **1 Nov**   | Submitted                                                                                                          |

These are suggested dates. Adjust them here if the team changes them, and record the change in section 6.

---

---

## 4. Status board

### Backend (source of truth)

| ID    | Feature                                | Pri | Status      | Owner  | Updated    | Notes                                                    |
| ----- | -------------------------------------- | --- | ----------- | ------ | ---------- | -------------------------------------------------------- |
| B0.1  | Backend stack decision                 | P0  | Done        | Haneef | 2026-11-01 | ADR-004 accepted: FastAPI + PostgreSQL, separate repo    |
| B0.2 | Service skeleton | P0 | Done        | Claude | 2026-11-01 | PR feat/B0.2-service-skeleton: FastAPI factory, /health, settings that fail fast, request ID, CORS, Dockerfile, CI. Done when CI is green on the PR |
| B0.3  | API contract (OpenAPI)                 | P0  | Done        |        | 2026-11-01 | Merged (PR #3). Models, 28 stub routes, `openapi.json`, error catalogue, frontend payload check. See `docs/api-contract.md` |
| B0.4 | Database and migrations | P0 | Done        | Claude | 2026-11-01 | SQLAlchemy 2 async, Alembic baseline, docker-compose (Postgres, MinIO), separate test DB, up/down/up migration test. Windows setup not yet verified on Windows |
| B0.5 | Test harness | P0 | Done        | Claude | 2026-11-01 | pytest with rollback-isolated sessions on real PostgreSQL. Entity factories and per-role clients land with B1.1 and B2.1 |
| B1.1  | Core schema                            | P0  | Not started |        |            |                                                          |
| B1.2  | Append-only audit log                  | P0  | Not started |        |            |                                                          |
| B1.3  | Demo seed data                         | P0  | Not started |        |            | Pilot organisation `[PLACEHOLDER]`                       |
| B2.1  | Staff authentication                   | P0  | Not started |        |            |                                                          |
| B2.2  | Authorisation and organisation scoping | P0  | Not started |        |            |                                                          |
| B2.3  | Current user                           | P0  | Not started |        |            |                                                          |
| B2.4  | Password reset                         | P2  | Not started |        |            |                                                          |
| B3.1  | Organisation registration              | P0  | Not started |        |            |                                                          |
| B3.2  | Verification documents                 | P0  | Not started |        |            |                                                          |
| B3.3  | Verify or reject organisation          | P0  | Not started |        |            |                                                          |
| B3.4  | Public organisation profile            | P1  | Not started |        |            |                                                          |
| B4.1  | Draft campaigns and items              | P0  | Not started |        |            |                                                          |
| B4.2  | Lifecycle state machine                | P0  | Not started |        |            |                                                          |
| B4.3  | Immutability after first donation      | P0  | Not started |        |            | Purpose lock depends on D8                               |
| B4.4  | Close early and end dates              | P0  | Not started |        |            | D10                                                      |
| B4.5  | Completion                             | P1  | Not started |        |            |                                                          |
| B5.1  | Campaign list                          | P0  | Not started |        |            |                                                          |
| B5.2  | Campaign detail and accountability     | P0  | Not started |        |            |                                                          |
| B5.3  | Live updates support                   | P0  | Not started |        |            |                                                          |
| B6.1  | Checkout with reservations             | P0  | Not started |        |            | D1 = offer remaining, D6 = 15 min                        |
| B6.2  | Reservation expiry                     | P0  | Not started |        |            |                                                          |
| B6.3  | Concurrency test suite                 | P0  | Not started |        |            |                                                          |
| B7.1  | Payment provider adapter               | P0  | Not started |        |            | D3 = Paystack test mode                                  |
| B7.2  | Initialise transaction                 | P0  | Not started |        |            |                                                          |
| B7.3  | Webhook confirmation                   | P0  | Not started |        |            |                                                          |
| B7.4  | Excess handling                        | P0  | Not started |        |            | D9 ruling pending                                        |
| B7.5  | Donation status                        | P0  | Not started |        |            |                                                          |
| B8.1  | File storage                           | P0  | Not started |        |            |                                                          |
| B8.2  | Evidence upload                        | P0  | Not started |        |            |                                                          |
| B8.3  | Log expense                            | P0  | Not started |        |            |                                                          |
| B8.4  | Item purchase status                   | P1  | Not started |        |            |                                                          |
| B9.1  | Witness assignment                     | P0  | Not started |        |            | D2 = in-app                                              |
| B9.2  | Delivery confirmation                  | P0  | Not started |        |            |                                                          |
| B9.3  | Campaign updates                       | P1  | Not started |        |            |                                                          |
| B10.1 | Organisation verification queue        | P0  | Not started |        |            |                                                          |
| B10.2 | Campaign review queue                  | P0  | Not started |        |            |                                                          |
| B10.3 | Excess resolution                      | P1  | Not started |        |            |                                                          |
| B10.4 | Audit log query                        | P1  | Not started |        |            |                                                          |
| B11.1 | Email adapter and receipt              | P1  | Not started |        |            | Gated by D11                                             |
| B11.2 | Milestone notifications                | P2  | Not started |        |            | Gated by D11                                             |
| B11.3 | Web push                               | P2  | Not started |        |            | Post-MVP                                                 |
| B12.1 | Security hardening                     | P0  | Not started |        |            |                                                          |
| B12.2 | Data protection (NDPA)                 | P0  | Not started |        |            |                                                          |
| B12.3 | Observability                          | P1  | Not started |        |            |                                                          |
| B12.4 | Deployment                             | P0  | Not started |        |            |                                                          |

---

---

## 5. Blockers

| Item | Blocked by | Since | Action needed |
| ---- | ---------- | ----- | ------------- |
| none | | | |

---

## 6. Open spec decisions that affect the roadmap

Defaults from spec §11 are assumed until the team decides. When one is decided, record an ADR and update the affected items.

| Decision                                | Default in use                              | Affects                 |
| --------------------------------------- | ------------------------------------------- | ----------------------- |
| D1: over-remaining donation             | Offer the remaining amount                  | F4.3, B6.1              |
| D2: witness channel                     | In-app                                      | F10, B9                 |
| D3: payment provider                    | Paystack test mode                          | B7                      |
| D4: settlement                          | Record only                                 | none in MVP             |
| D5: tech stack                          | Frontend ADR-001. Backend ADR-004 (FastAPI) | B0                      |
| D6: reservation TTL                     | 15 minutes                                  | B6.1, B6.2              |
| D7: donor accounts                      | Guest only                                  | F4.2                    |
| D8: proposed Sharia rules               | None until approved                         | F4.2, F7.6, F11.2, B4.3 |
| D9: scholarly advisor and excess ruling | `[PLACEHOLDER]`                             | B7.4, F11.3             |
| D10: campaign end dates                 | Optional                                    | F7.2, B4.4              |
| D11: email receipts                     | `[PLACEHOLDER]`                             | B11                     |

---

---

## 7. Index change log

| Date | Change | By |
| ---- | ------ | -- |
| 2026-11-01 | B0.2 to B0.5 done (skeleton, contract, database, tests); Python 3.14 and FastAPI 0.162 adopted. Earlier: B0.2, B0.4, B0.5 in progress: service skeleton, database layer and test harness in one PR. | Claude |
| 2026-11-01 | Repository created with the spec, backend roadmap and ADRs. B0.1 done (ADR-004). ADR-011 to ADR-013 accepted. | Claude |
