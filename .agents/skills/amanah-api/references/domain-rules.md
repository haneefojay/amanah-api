# Amanah domain rules (backend)

Source of truth: `docs/amanah-mvp-spec.md`. Backend non-negotiables are also in `docs/roadmap/BACKEND_ROADMAP.md`. This file condenses the rules an implementer must not get wrong. If this file and the spec disagree, the spec wins — flag the mismatch.

## Contents

1. Money
2. The donation cap (spec §4)
3. Campaign lifecycle (spec §5)
4. Roles and access (spec §3)
5. Evidence and witnesses (spec §7)
6. Privacy (spec §9, NDPA)
7. Copy and terminology
8. Open decisions and their defaults (spec §11)

---

## 1. Money

- Unit: **kobo**, integer. ₦1 = 100 kobo. ₦500,000 = `50_000_000`.
- API fields are kobo integers (`targetAmount`, `raisedAmount`, `availableAmount`). Pydantic type: `int` with `ge=0`. Database columns are `BIGINT`. **Never `float`, never `Decimal` for money.**
- The frontend formats and parses naira; the API only ever sees and returns kobo.
- Item totals: `total_cost = quantity × unit_cost` (integers). **Sum of item totals must equal `target_amount`.**
- Derived values on the accountability page:
  - Remaining to raise = `target − raised`
  - Spent = Σ expenses
  - Balance held = `raised − spent`
  - Progress = `raised / target`
- Total expenses can never exceed `raised`.

## 2. The donation cap (spec §4)

The organisation may never receive more than its target.

- `available = target − raised − active reservations`. The API returns it as `availableAmount`.
- Checkout creates a **reservation** (default TTL 15 min, D6) inside a locked DB transaction; the reservation ID is the payment reference.
- Over-remaining (D1 default: **offer the remaining amount**): the API returns `409 AMOUNT_EXCEEDS_AVAILABLE` with `availableAmount`; the frontend offers "Give ₦X instead" / Cancel.
- `409 TARGET_REACHED` when `available == 0`; `409 CAMPAIGN_NOT_ACCEPTING` when not LIVE.
- Confirmation only via verified webhook. The result page polls `GET /api/donations/:reference` and **never claims success before the backend confirms**.
- Late payment beyond target → `ExcessRecord` (`PENDING_RETURN` → `RETURNED` or `SENT_TO_BAYT_AL_MAL`), handled manually by a platform admin.

The API returns `availableAmount`, `raisedAmount` and the campaign `status`; the frontend renders the exact spec copy for each state ("Target reached. Donations closed.", "Target nearly reached. Pending payments are being processed."). The backend never lets the client decide whether a donation is allowed.

---

## 3. Campaign lifecycle (spec §5)

```
DRAFT → PENDING_REVIEW → LIVE → FUNDED (automatic at target) → COMPLETED
              ↓            ↓
          REJECTED       CLOSED (org ends early / end date) → COMPLETED
              ↓
            DRAFT
```

- Only `LIVE` accepts donations.
- Expenses, evidence and witness confirmations allowed in `LIVE`, `FUNDED`, `CLOSED`.
- `target_amount` is **immutable after the first donation** (and title/purpose/items too if D8 purpose lock is approved — not yet).
- Only a `VERIFIED` organisation can submit a campaign.
- The API rejects any transition the diagram does not allow for the caller's role (B4.2).

## 4. Roles and access (spec §3)

| Role                           | Area         | Can                                                                                   |
| ------------------------------ | ------------ | ------------------------------------------------------------------------------------- |
| Donor (guest, no account — D7) | public       | browse, donate, view accountability                                                   |
| `ORG_ADMIN`                    | `/org/*`     | own organisation only: campaigns, expenses, evidence, updates, witnesses, close early |
| `WITNESS`                      | `/witness/*` | assigned campaigns only: confirm or dispute delivery                                  |
| `PLATFORM_ADMIN`               | `/admin/*`   | verify orgs, review campaigns, resolve excess, read audit log                         |

- A witness **cannot** be an admin of the organisation running the campaign (`409 WITNESS_CONFLICT`).
- Every protected endpoint returns 401 without a session and 403 for the wrong role or organisation (B2.2). Sessions live in an httpOnly cookie, never in `localStorage` (ADR-011).

## 5. Evidence and witnesses (spec §7)

- The frontend captures the photo and location and sends the client capture time with the upload.
- **Server upload time is authoritative.** The API sets it; the client time is stored only as secondary data.
- Location may be missing (permission denied); accept the upload and store no coordinates.
- Validate content type and size; evidence is image-only (B8.1, ADR-013).
- Honest limitation: a browser can't prove a photo came from the camera. Trust signal = location + server timestamp + witness confirmation.
- A **disputed** item can never be shown or marked as delivered. Dispute requires a comment.

## 6. Privacy (spec §9, Nigeria Data Protection Act)

- Collect only name, email, phone at checkout.
- Public API responses never include donor email or phone (a test scans public responses, B12.2).
- Anonymous giving toggle only if D8 approves it.

## 7. Copy and terminology

- British spelling ("organisation", "colour") in messages and docs; Nigerian context (₦, Africa/Lagos time). Store timestamps in UTC and return ISO 8601.
- Never: zakat, zakah, waqf, awqaf (out of scope permanently).
- Islamic terms already in the spec: Amanah, Sharia, riba, Bayt al-Mal (excess handling). Confirm with the team before introducing any other religious terminology.

## 8. Open decisions (spec §11) — defaults in use

| ID  | Topic                                                         | Default (until the team decides)                   |
| --- | ------------------------------------------------------------- | -------------------------------------------------- |
| D1  | Over-remaining donation                                       | Offer remaining amount                             |
| D2  | Witness channel                                               | In-app                                             |
| D3  | Payment provider                                              | Paystack test mode                                 |
| D4  | Settlement                                                    | Record only                                        |
| D5  | Stack                                                         | Frontend ADR-001. Backend ADR-004 (FastAPI)        |
| D6  | Reservation TTL                                               | 15 min                                             |
| D7  | Donor accounts                                                | Guest only                                         |
| D8  | Purpose lock, no riba, permissible purposes, anonymous giving | **None** until approved — don't build them         |
| D9  | Scholarly advisor / excess ruling                             | Placeholder                                        |
| D10 | End dates                                                     | Optional                                           |
| D11 | Email receipts                                                | Placeholder — on-screen receipt is always required |

Changing any default needs the user's decision and an ADR.
