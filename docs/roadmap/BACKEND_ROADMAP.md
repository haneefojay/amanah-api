# Amanah Backend Roadmap

**Scope:** the Amanah API service described in [`docs/amanah-mvp-spec.md`](../amanah-mvp-spec.md). It is a separate service from the Next.js frontend ([ADR-003](../decisions/ADR-003-frontend-backend-separation.md)).
**Stack:** Python, FastAPI, PostgreSQL, SQLAlchemy 2 and Alembic ([ADR-004](../decisions/ADR-004-backend-stack.md), Accepted 2026-11-01). Auth is written by hand ([ADR-011](../decisions/ADR-011-authentication.md)), hosting starts on Railway ([ADR-012](../decisions/ADR-012-hosting-railway.md)) and files live in MinIO ([ADR-013](../decisions/ADR-013-object-storage-minio.md)).
**Repository:** this one (`haneefojay/amanah-api`). The frontend is `haneefojay/amanah`; the `F…` items cited below are in its [`FRONTEND_ROADMAP.md`](https://github.com/haneefojay/amanah/blob/main/docs/roadmap/FRONTEND_ROADMAP.md).
**Companion:** [`FRONTEND_ROADMAP.md`](./FRONTEND_ROADMAP.md). **Status tracking lives in [`ROADMAP_INDEX.md`](./ROADMAP_INDEX.md).**
**Created:** 18 October 2026. **Submission deadline:** 1 November 2026.

---

## How to read this roadmap

- **Phase:** `B<n>`. **Feature:** `B<n>.<m>`. IDs are permanent: never renumber. Dropped items stay listed as `Dropped` in the index.
- **Unblocks:** the frontend features (`F<n>.<m>`) waiting on each item. Prioritise backend items that unblock P0 frontend work.
- **Priority:** P0 (demo or acceptance criterion), P1 (solid MVP), P2 (post-MVP). Same meaning as in the frontend roadmap.
- **Spec references:** `§` numbers point to the MVP spec.

### Non-negotiables (from spec §4 and §9)

These apply to every item. A reviewer rejects any PR that breaks one of them.

1. **Money is integer kobo.** No floating-point types in code, database columns or JSON.
2. **The cap is enforced in the database transaction** with row locks (`SELECT … FOR UPDATE` or equivalent), never only in application memory.
3. **Webhooks are verified twice:** check the signature, then call the provider's verify endpoint. Never trust the body alone.
4. **Idempotency:** a unique constraint on `provider_reference`, and every webhook is safe to replay.
5. **Append-only audit log** for every state change, expense, evidence upload and confirmation.
6. **Access control on every non-public endpoint:** role check plus organisation scoping.
7. **Secrets only in environment variables**, never committed and never sent to the client.
8. **Public responses never include donor email or phone** (Nigeria Data Protection Act).

---

## Global Definition of Done (applies to every feature)

- [ ] Merged to `main` via a reviewed PR whose title contains the feature ID.
- [ ] **Tests are written and pass:**
  - unit tests for domain logic (state transitions, money arithmetic, validation);
  - **integration tests against a real PostgreSQL** (not mocks or SQLite) for every endpoint, covering success, validation failure, auth failure (401), permission failure (403) and not-found;
  - concurrency tests wherever the spec mentions locking or idempotency.
- [ ] The endpoint is documented in the OpenAPI contract (B0.3), with request, response and error codes. The contract change is announced to the frontend (the matching `F` feature updates its Zod schema and MSW handler).
- [ ] Errors use the standard envelope: `{ "error": { "code": "SCREAMING_SNAKE", "message": "…" } }`.
- [ ] An audit log entry is written for every mutation in scope of §9.
- [ ] No secrets in code. New configuration is added to `.env.example` with a comment.
- [ ] Database changes are delivered as migrations and are reversible or explicitly marked irreversible.
- [ ] CI is green. `ROADMAP_INDEX.md` and `CHANGELOG.md` are updated.
- [ ] Any decision is recorded as an ADR.

---

## B0: Foundation and stack decision

**Goal:** a running, tested, deployable API skeleton with an agreed contract.

### B0.1 Backend stack decision (P0) — Done 2026-11-01

- **Scope:** decide the language, framework, ORM or query layer, auth approach, file storage, job runner and hosting. Accept ADR-004.
- **Unblocks:** everything in B.
- **Tests:** not applicable.
- **Definition of Done:** ADR-004 is Accepted with options, trade-offs and the date. This roadmap's B0.2 to B0.5 are updated with concrete tools.

### B0.2 Service skeleton (P0)

- **Scope:** FastAPI project layout managed with `uv`, configuration loading with validation (`pydantic-settings`; fail fast on missing env vars), structured logging with a request ID, a `Dockerfile`, a `GET /health` endpoint (checks the database), CORS allowing the frontend origin with credentials, and a request ID.
- **Tools (ADR-004):** `uv`, FastAPI, `pydantic-settings`, Ruff, a type checker (mypy or pyright), pytest.
- **Unblocks:** all.
- **Tests:** an integration test for `/health`, and a test that startup fails with a missing required env var.
- **Definition of Done:** runs locally with one command, and the CI pipeline runs lint, type checks and tests.

### B0.3 API contract (OpenAPI) (P0)

- **Scope:** an OpenAPI 3.1 document covering every §8 endpoint, plus auth (`/api/auth/*`, `/api/me`), organisation registration, and list endpoints for dashboards. Standard error codes catalogue, pagination convention and date format (ISO 8601 UTC). FastAPI generates it from the code; the exported `openapi.json` is committed and CI fails if it is out of date. Served at `/api/docs`.
- **Unblocks:** **F0.4** (contract sync) and every frontend feature's integration.
- **Tests:** contract tests check responses against the schema in the integration suite.
- **Definition of Done:** the frontend can generate types from it, and the draft frontend schemas (`src/lib/api/schemas.ts`) are reconciled with it.

### B0.4 Database and migrations (P0)

- **Scope:** PostgreSQL (required by spec §8 for row locking), SQLAlchemy 2.x models, Alembic migrations, a local database through Docker Compose (PostgreSQL and MinIO), and a separate test database.
- **Unblocks:** B1 onwards.
- **Tests:** migrations apply on an empty database in CI and can be rolled back.
- **Definition of Done:** documented one-command setup for a new developer on Windows.

### B0.5 Test harness (P0)

- **Scope:** pytest (with `pytest-asyncio` and `httpx`) for unit and integration tests, per-test database isolation (transactions or truncation), factories for every entity, and an authenticated test-client helper for each role.
- **Unblocks:** all.
- **Tests:** example tests for each layer.
- **Definition of Done:** the full suite runs in CI against PostgreSQL in under 5 minutes.

### B0.6 Modular monolith structure (P0)

- **Scope:** restructure the API into `app/core`, `app/db` and `app/modules/{auth, organisations, campaigns, donations, accountability, audit, admin}` as decided in ADR-015, keeping all 28 contract routes and `openapi.json` unchanged.
- **Unblocks:** B1 onwards (each module adds its own `models.py` and `service.py`).
- **Tests:** an architecture test fails on cross-module internal imports, import cycles and upward imports from `core` and `db`; the existing contract tests and the stale-`openapi.json` check keep passing.
- **Definition of Done:** the full suite, Ruff and mypy pass, and `openapi.json` is byte-identical to before.

**Phase B0 Definition of Done:** ADR-004 accepted (done), `/health` deployed to a staging URL, OpenAPI v0 published, and CI green.

---

## B1: Data model and audit

### B1.1 Core schema (P0)

- **Scope:** every entity in spec §6 (User, Organisation, OrganisationMember, Campaign, CampaignItem, Reservation, Donation, ExcessRecord, Expense, Evidence, WitnessAssignment, DeliveryConfirmation, CampaignUpdate, AuditLog) with UUID ids, `created_at` and `updated_at`, kobo integers (`BIGINT`), enums, foreign keys, and these database constraints:
  - `Donation.provider_reference` UNIQUE;
  - `CHECK (amount > 0)` on money columns;
  - `CHECK (raised_amount <= target_amount)` on Campaign;
  - indexes on `campaign_id`, `status` and `expires_at`.
- **Unblocks:** all.
- **Tests:** a migration test, plus constraint tests (inserting a violating row fails at the database level).
- **Definition of Done:** the entity relationship diagram is committed in `docs/`, and every rule in the §6 "Rules" column is enforced by a constraint or a tested service rule.

### B1.2 Append-only audit log (P0)

- **Scope:** an `audit_log` table and service `audit.record(actor, action, entityType, entityId, payload)` called inside the same transaction as the change. Enforce append-only at the database level (revoke UPDATE and DELETE, or a trigger that raises).
- **Unblocks:** **F11.4**.
- **Tests:** an integration test that UPDATE or DELETE on `audit_log` fails, and a test that a rolled-back transaction leaves no audit row.
- **Definition of Done:** the §9 audit list is covered (state changes, expenses, evidence, confirmations).

### B1.3 Demo seed data (P0)

- **Scope:** an idempotent seed script: platform admin, a pending organisation for demo step 1 (pilot organisation `[PLACEHOLDER]`), org admin, witness, sample campaigns in several states, and realistic Nigerian names and cities.
- **Unblocks:** **F13.4** and **F13.5**.
- **Tests:** the seed runs twice without errors or duplicates.
- **Definition of Done:** the demo script can start from a freshly seeded database.

---

## B2: Authentication and access control

### B2.1 Staff authentication (P0)

- **Scope:** `POST /api/auth/login` and `POST /api/auth/logout`. Written by hand (ADR-011), with no external auth service: passwords hashed with argon2id, opaque server-side sessions stored in PostgreSQL (token hashed at rest) and sent as an httpOnly, Secure, SameSite cookie, plus CSRF protection for state-changing requests. Rate-limited login. Generic error messages.
- **Unblocks:** **F5.1**.
- **Tests:** login success and failure, a locked-out rate limit, the cookie flags, and logout invalidating the session.
- **Definition of Done:** no password or hash ever appears in logs or responses.

### B2.2 Authorisation and organisation scoping (P0)

- **Scope:** role guard middleware (`ORG_ADMIN`, `WITNESS`, `PLATFORM_ADMIN`), an organisation-membership check for every `/api/org/*` resource, and an assignment check for every `/api/witness/*` resource.
- **Unblocks:** **F5.3**.
- **Tests:** a matrix test: for every protected endpoint, each role and a non-member receive the correct 401 or 403.
- **Definition of Done:** the matrix test covers 100% of protected endpoints, enforced by a test that lists routes.

### B2.3 Current user (P0)

- **Scope:** `GET /api/me` returns the user, role and organisation memberships.
- **Unblocks:** **F1.4** and **F5.2**.
- **Tests:** authenticated and anonymous cases.
- **Definition of Done:** documented in the contract.

### B2.4 Password reset (P2)

- **Scope:** request a reset token by email, and set a new password.
- **Unblocks:** **F5.4**.
- **Tests:** token expiry and single use.
- **Definition of Done:** only if time allows. Otherwise the platform admin resets passwords manually.

---

## B3: Organisations

### B3.1 Organisation registration (P0)

- **Scope:** `POST /api/organisations` creates the Organisation (PENDING), the first ORG_ADMIN user and the membership in one transaction.
- **Unblocks:** **F6.1**.
- **Tests:** success, duplicate email, validation errors, and an audit entry.
- **Definition of Done:** the new organisation appears in the admin verification queue.

### B3.2 Verification documents (P0)

- **Scope:** attach documents to the organisation (via B8.1 storage). Allowed types: image or PDF, with a size limit.
- **Unblocks:** **F6.2**.
- **Tests:** type and size rejection, and only members can upload.
- **Definition of Done:** documents are viewable only by the organisation's members and platform admins (signed URLs).

### B3.3 Verify or reject organisation (P0)

- **Scope:** `POST /api/admin/organisations/:id/verify` with `{ decision, notes }`. Only `VERIFIED` organisations can submit campaigns.
- **Unblocks:** **F6.3** and **F11.1**.
- **Tests:** a state transition test, the rule that an unverified organisation cannot submit a campaign (acceptance criterion), and an audit entry.
- **Definition of Done:** acceptance criterion "An unverified organisation cannot publish a campaign" passes at the API level.

### B3.4 Public organisation profile (P1)

- **Scope:** `GET /api/organisations/:id` for verified organisations only, including past campaigns and a completion record.
- **Unblocks:** **F2.4**.
- **Tests:** an unverified organisation returns 404, and no private fields are leaked.
- **Definition of Done:** documented in the contract.

---

## B4: Campaigns and lifecycle

### B4.1 Draft campaigns and items (P0)

- **Scope:** `POST /api/org/campaigns` and `PATCH /api/org/campaigns/:id` (DRAFT only), item create, update and delete, `GET /api/org/campaigns` (own campaigns), and a donations-received list for the organisation. Slug generation. Validation: **sum of item `total_cost` equals `target_amount`** at submit time, and `total_cost = quantity × unit_cost` computed on the server.
- **Unblocks:** **F7.1**, **F7.2** and **F7.4**.
- **Tests:** CRUD, the sum mismatch error code `ITEMS_TOTAL_MISMATCH`, and that another organisation's draft returns 403.
- **Definition of Done:** documented in the contract with every error code.

### B4.2 Lifecycle state machine (P0)

- **Scope:** implement the §5 state diagram as a single tested transition function. Submit (DRAFT to PENDING_REVIEW, verified organisations only), approve (to LIVE, sets `published_at`), reject (with a reason), edit after rejection (REJECTED to DRAFT). Illegal transitions return 409 `INVALID_TRANSITION`.
- **Unblocks:** **F7.3** and **F11.2**.
- **Tests:** a table-driven test of every legal and illegal transition, plus an audit entry per transition.
- **Definition of Done:** the transition table in code matches §5 exactly.

### B4.3 Immutability after first donation (P0)

- **Scope:** reject changes to `target_amount` once any donation exists (and title, purpose and items too if D8 purpose lock is approved). Expose `hasDonations` in the organisation's campaign response.
- **Unblocks:** **F7.6**.
- **Tests:** an attempt to edit the target after a donation returns 409 `TARGET_LOCKED` (acceptance criterion).
- **Definition of Done:** the acceptance criterion passes.

### B4.4 Close early and end dates (P0)

- **Scope:** `POST /api/org/campaigns/:id/close` (LIVE to CLOSED). If D10 keeps end dates optional, a scheduled job or lazy check closes campaigns past `end_date`. Cancel active reservations on close.
- **Unblocks:** **F7.5**.
- **Tests:** close, checkout after close is rejected, and end-date expiry.
- **Definition of Done:** a closed campaign accepts no checkouts.

### B4.5 Completion (P1)

- **Scope:** move FUNDED or CLOSED to COMPLETED automatically when all (funded) items are delivered and confirmed.
- **Unblocks:** **F3.1** (status) and **F2.4** (completion record).
- **Tests:** completion triggers after the last confirmation, and a disputed item blocks completion.
- **Definition of Done:** the final report state is visible publicly.

---

## B5: Public read API and accountability

### B5.1 Campaign list (P0)

- **Scope:** `GET /api/campaigns` lists LIVE, FUNDED, CLOSED and recently COMPLETED campaigns, with filters `city` and `organisationId`, pagination, and summary fields including `availableAmount`.
- **Unblocks:** **F2.1** and **F2.2**.
- **Tests:** filtering, pagination, and that DRAFT, PENDING_REVIEW and REJECTED are never listed.
- **Definition of Done:** p95 response time under 300 ms with 100 campaigns seeded.

### B5.2 Campaign detail with accountability data (P0)

- **Scope:** `GET /api/campaigns/:slug` returns the campaign, organisation summary, items with delivery confirmation, expenses with receipt URLs, evidence (location, client and server time), updates, and derived values (`remaining`, `spent`, `balanceHeld`, `progress`, `availableAmount`). No donor contact data.
- **Unblocks:** **F2.3**, **F3.1**, **F3.2**, **F3.5**, **F4.1** and **F7.4**.
- **Tests:** the derived values match the §6 formulas, the response contains no email or phone (privacy test), and unpublished campaigns return 404.
- **Definition of Done:** a single request renders the whole accountability section.

### B5.3 Live updates support (P0)

- **Scope:** at minimum, ETag or `Last-Modified` with `304` support on B5.2 for cheap polling. Optional Server-Sent Events stream `GET /api/campaigns/:slug/events`.
- **Unblocks:** **F3.7**.
- **Tests:** a 304 when unchanged and a 200 after a donation is confirmed.
- **Definition of Done:** demo step 3 updates within 15 seconds.

---

## B6: Donation cap and checkout (spec §4)

The highest-risk part of the system. Review every change here with two people.

### B6.1 Checkout with reservations (P0)

- **Scope:** `POST /api/campaigns/:id/checkout` with `{ amount, donorName, donorEmail, donorPhone, isAnonymous? }`. In one transaction: lock the campaign row, compute `available = target − raised − active reserved`, and apply **D1 (offer the remaining amount)**:
  - `amount > available > 0` returns 409 `AMOUNT_EXCEEDS_AVAILABLE` with `availableAmount`;
  - `available == 0` returns 409 `TARGET_REACHED`;
  - a campaign that is not LIVE returns 409 `CAMPAIGN_NOT_ACCEPTING`.

  Otherwise it creates a Reservation (ACTIVE, `expires_at = now + TTL`, D6 default 15 minutes) and initialises the payment (B7.2) using the reservation ID as the reference.

- **Unblocks:** **F4.1**, **F4.2** and **F4.3**.
- **Tests:** each error code, amount validation (positive integer kobo), and that the reservation is not created when payment initialisation fails (or is cancelled).
- **Definition of Done:** demo step 4 behaves as specified.

### B6.2 Reservation expiry (P0)

- **Scope:** a lazy expiry check inside the checkout transaction, plus a periodic job that marks past-due ACTIVE reservations as EXPIRED and releases them.
- **Unblocks:** **F4.1** (accurate "nearly reached" state).
- **Tests:** an expired reservation frees `available` (acceptance criterion), and the job is idempotent.
- **Definition of Done:** the acceptance criterion "Expired reservations release their amount" passes.

### B6.3 Concurrency test suite (P0)

- **Scope:** an automated test that fires **20 parallel checkouts plus confirmations** whose total exceeds the remaining amount, and asserts the confirmed total is at most the target and there is no negative `available` (spec §10). Also tests races between expiry and confirmation.
- **Unblocks:** confidence for the demo.
- **Tests:** the suite itself, run in CI against real PostgreSQL.
- **Definition of Done:** green 50 times in a row locally (flakiness check), then kept in CI.

---

## B7: Payments (Paystack test mode)

### B7.1 Payment provider adapter (P0)

- **Scope:** an interface `initialise`, `verify` and `verifyWebhookSignature`, with a **Paystack test-mode** implementation (D3) and a **mock provider** for local work and deterministic e2e runs.
- **Unblocks:** **F4.4** and **F13.4**.
- **Tests:** unit tests for the Paystack request mapping (amount in kobo, reference) and signature verification (HMAC-SHA512) using recorded fixtures.
- **Definition of Done:** switchable by env var, and the mock provider can simulate success, failure and late payment.

### B7.2 Initialise transaction (P0)

- **Scope:** part of the checkout response: `{ reference, authorizationUrl, expiresAt }`. The callback URL points to the frontend `/donations/[reference]`.
- **Unblocks:** **F4.4**.
- **Tests:** an integration test with the mock provider.
- **Definition of Done:** the frontend can redirect and return.

### B7.3 Webhook confirmation (P0)

- **Scope:** `POST /api/webhooks/payments`:
  1. verify the signature;
  2. call the provider's verify endpoint;
  3. in one transaction, lock the campaign and reservation, create the Donation, mark the reservation CONFIRMED and increment `raised_amount`;
  4. move to FUNDED at target (sets `funded_at` and cancels other ACTIVE reservations);
  5. respond 200 quickly.

  Idempotent on `provider_reference`.

- **Unblocks:** **F3.7**, **F4.5** and **F7.4**.
- **Tests:**
  - an invalid signature returns 401;
  - a body mismatching the verify result is rejected;
  - **replaying the same webhook 5 times creates one donation** (acceptance criterion);
  - FUNDED is set exactly at target.
- **Definition of Done:** the acceptance criteria "Campaign moves to FUNDED automatically" and "A replayed webhook does not create a duplicate donation" pass.

### B7.4 Excess handling (P0)

- **Scope:** a late payment after expiry when the campaign is full or partly full. Confirm only up to the remaining amount, record the rest as an ExcessRecord (PENDING_RETURN), write to the audit log, and alert the platform admin (email if D11 is in, otherwise a dashboard flag).
- **Unblocks:** **F11.3**.
- **Tests:** a late payment beyond target creates an ExcessRecord and `raised` never exceeds the target (acceptance criterion).
- **Definition of Done:** the acceptance criterion passes.

### B7.5 Donation status (P0)

- **Scope:** `GET /api/donations/:reference` returns `{ status: PENDING | SUCCESS | FAILED | EXPIRED, amount, campaignSlug, receiptReference }`, with no personal data beyond what the donor entered.
- **Unblocks:** **F4.5**.
- **Tests:** each status, and an unknown reference returns 404.
- **Definition of Done:** the result page can show the outcome reliably.

---

## B8: Expenses and evidence

### B8.1 File storage (P0)

- **Scope:** an S3-compatible object storage adapter backed by MinIO (ADR-013), signed upload URLs or a multipart endpoint, content-type and size validation, and image-only for evidence. Public read URLs for published evidence and private signed URLs for verification documents.
- **Unblocks:** **F6.2** and **F8.3**.
- **Tests:** type and size rejection, and that signed URLs expire.
- **Definition of Done:** no storage credentials ever reach the client.

### B8.2 Evidence upload (P0)

- **Scope:** `POST /api/org/campaigns/:id/evidence` with `{ type: RECEIPT | PHOTO, fileKey, latitude?, longitude?, capturedAtClient? }`. The server sets `uploaded_at_server` (authoritative) and `uploaded_by`. Allowed in LIVE, FUNDED and CLOSED.
- **Unblocks:** **F3.4** and **F8.1**.
- **Tests:** the server timestamp is set regardless of client input (acceptance criterion "Evidence stores location and server timestamp"), the wrong-state rejection, and an audit entry.
- **Definition of Done:** the acceptance criterion passes.

### B8.3 Log expense (P0)

- **Scope:** `POST /api/org/campaigns/:id/expenses` with a required receipt evidence reference. Lock the campaign, then reject if `sum(expenses) + amount > raised_amount` with 409 `EXPENSES_EXCEED_RAISED`.
- **Unblocks:** **F3.3** and **F8.4**.
- **Tests:** the over-limit rejection (acceptance criterion), a concurrent expense race, and an audit entry.
- **Definition of Done:** the acceptance criterion "Total expenses cannot exceed raised amount" passes.

### B8.4 Item purchase status (P1)

- **Scope:** update an item to PURCHASED (via expense link or explicitly).
- **Unblocks:** **F8.5**.
- **Tests:** the transition rules (DELIVERED only through witness confirmation).
- **Definition of Done:** documented in the contract.

---

## B9: Witnesses and updates

### B9.1 Witness assignment (P0)

- **Scope:** `POST /api/org/campaigns/:id/witnesses` assigns by email, creating a WITNESS user with an invite if they don't exist. Reject when the user is an admin of the campaign's organisation (409 `WITNESS_CONFLICT`). `GET /api/witness/campaigns` lists the witness's assignments.
- **Unblocks:** **F9.2** and **F10.1**.
- **Tests:** the conflict rule (acceptance criterion), and that a witness sees only assigned campaigns.
- **Definition of Done:** the acceptance criterion "A witness cannot be an admin of the same organisation" passes.

### B9.2 Delivery confirmation (P0)

- **Scope:** `POST /api/witness/items/:id/confirm` with `{ status: CONFIRMED | DISPUTED, comment }` (a comment is required for a dispute). CONFIRMED sets the item to DELIVERED. DISPUTED blocks DELIVERED until resolved. Triggers the B4.5 completion check.
- **Unblocks:** **F3.2** and **F10.2**.
- **Tests:** a disputed item cannot become DELIVERED (acceptance criterion), only the assigned witness can confirm, and an audit entry.
- **Definition of Done:** the acceptance criterion passes.

### B9.3 Campaign updates (P1)

- **Scope:** `POST /api/org/campaigns/:id/updates` with a body and optional image keys. Included in B5.2.
- **Unblocks:** **F3.6** and **F9.1**.
- **Tests:** create, length validation and ordering.
- **Definition of Done:** documented in the contract.

---

## B10: Platform admin

### B10.1 Organisation verification queue (P0)

- **Scope:** `GET /api/admin/organisations?status=PENDING` with documents.
- **Unblocks:** **F11.1**.
- **Tests:** platform admins only.
- **Definition of Done:** demo step 1 works against the API.

### B10.2 Campaign review queue (P0)

- **Scope:** `GET /api/admin/campaigns?status=PENDING_REVIEW` and `POST /api/admin/campaigns/:id/review` with `{ decision, reason }`.
- **Unblocks:** **F11.2**.
- **Tests:** approve and reject transitions, a reason is required for rejection, and platform admins only.
- **Definition of Done:** demo step 2 (approval) works.

### B10.3 Excess resolution (P1)

- **Scope:** `GET /api/admin/excess` and `PATCH /api/admin/excess/:id` with `{ status: RETURNED | SENT_TO_BAYT_AL_MAL, notes }`. Sets `resolved_by` and writes to the audit log.
- **Unblocks:** **F11.3**.
- **Tests:** transitions, notes required, and audit entry.
- **Definition of Done:** the R5 manual action is supported.

### B10.4 Audit log query (P1)

- **Scope:** `GET /api/admin/audit` with filters (actor, entity, action, date range) and pagination. Read-only.
- **Unblocks:** **F11.4**.
- **Tests:** filters, pagination and access control.
- **Definition of Done:** every demo action is queryable.

---

## B11: Notifications (gated by D11)

### B11.1 Email adapter and donor receipt (P1, pending D11)

- **Scope:** an email provider adapter (console transport in development), and a donor receipt email after confirmation (sent outside the payment transaction, with retry).
- **Unblocks:** the receipt mention in **F4.5**.
- **Tests:** a receipt is queued after confirmation exactly once, even on webhook replay.
- **Definition of Done:** only if D11 is "In". Otherwise it is marked Dropped and the on-screen receipt is used.

### B11.2 Milestone notifications (P2, pending D11)

- **Scope:** emails to donors on FUNDED and COMPLETED.
- **Unblocks:** none in the MVP.
- **Tests:** one notification per milestone.
- **Definition of Done:** only if D11 is "In" and time allows.

### B11.3 Web push (P2, post-MVP)

- **Scope:** store push subscriptions and send them via VAPID.
- **Unblocks:** **F12.5**.
- **Tests:** to be defined.
- **Definition of Done:** post-MVP.

---

## B12: Security, compliance and deployment

### B12.1 Security hardening (P0)

- **Scope:** input validation on every endpoint, rate limiting (login, checkout, webhook), CORS restricted to the frontend origins, security headers, dependency audit in CI, and no stack traces in production errors.
- **Unblocks:** release.
- **Tests:** rate-limit tests, a CORS test, and a fuzz test on the checkout amount.
- **Definition of Done:** a checklist in `docs/security-checklist.md` is complete.

### B12.2 Data protection, NDPA (P0)

- **Scope:** collect the minimum donor data, keep public responses free of contact data, set a retention note, and add a privacy policy text endpoint or content.
- **Unblocks:** **F4.6**.
- **Tests:** an automated scan of public endpoint responses for email and phone patterns.
- **Definition of Done:** the team has reviewed it.

### B12.3 Observability (P1)

- **Scope:** structured logs with request ID, error tracking, and a payment webhook log (no secrets).
- **Unblocks:** smooth demo debugging.
- **Tests:** a log redaction test (no card data, secrets or passwords).
- **Definition of Done:** errors on staging are visible within one minute.

### B12.4 Deployment (P0)

- **Scope:** staging and production environments on Railway (ADR-012) with its PostgreSQL service and backups, a MinIO service with a persistent volume, environment secrets, the HTTPS API domain, a webhook URL registered with Paystack (test), and migrations run on deploy.
- **Unblocks:** **F0.6**, **F13.4** and **F13.5**.
- **Tests:** a smoke test after deploy (`/health`, list campaigns).
- **Definition of Done:** the frontend production build points at the production API, and the demo script passes on production.

---

## Cross-reference: backend to frontend

| Backend | Unblocks frontend                        |
| ------- | ---------------------------------------- |
| B0.3    | F0.4 and all integrations                |
| B1.2    | F11.4                                    |
| B1.3    | F13.4, F13.5                             |
| B2.1    | F5.1                                     |
| B2.2    | F5.3                                     |
| B2.3    | F1.4, F5.2                               |
| B2.4    | F5.4                                     |
| B3.1    | F6.1                                     |
| B3.2    | F6.2                                     |
| B3.3    | F6.3, F11.1                              |
| B3.4    | F2.4                                     |
| B4.1    | F7.1, F7.2, F7.4                         |
| B4.2    | F7.3, F11.2                              |
| B4.3    | F7.6                                     |
| B4.4    | F7.5                                     |
| B4.5    | F3.1, F2.4                               |
| B5.1    | F2.1, F2.2                               |
| B5.2    | F2.3, F2.5, F3.1, F3.2, F3.5, F4.1, F7.4 |
| B5.3    | F3.7                                     |
| B6.1    | F4.1, F4.2, F4.3                         |
| B6.2    | F4.1                                     |
| B7.1    | F4.4, F13.4                              |
| B7.2    | F4.4                                     |
| B7.3    | F3.7, F4.5, F7.4                         |
| B7.4    | F11.3                                    |
| B7.5    | F4.5, F7.4                               |
| B8.1    | F6.2, F8.3                               |
| B8.2    | F3.4, F8.1                               |
| B8.3    | F3.3, F8.4                               |
| B8.4    | F8.5                                     |
| B9.1    | F9.2, F10.1                              |
| B9.2    | F3.2, F10.2                              |
| B9.3    | F3.6, F9.1                               |
| B10.1   | F11.1                                    |
| B10.2   | F11.2                                    |
| B10.3   | F11.3                                    |
| B10.4   | F11.4                                    |
| B11.3   | F12.5                                    |
| B12.2   | F4.6                                     |
| B12.4   | F0.6, F13.4, F13.5                       |
