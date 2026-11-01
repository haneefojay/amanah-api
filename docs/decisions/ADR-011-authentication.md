# ADR-011: Hand-written authentication with server-side sessions

- **Status:** Accepted
- **Date:** 2026-11-01
- **Deciders:** Project owner (Haneef)
- **Related:** spec §3, §9; BACKEND_ROADMAP B2.1 to B2.4, B12.1; ADR-003; ADR-004; frontend F1.4, F5.1

## Context

Staff users (organisation admins, witnesses, platform admins) need to sign in. Donors are guests (D7). The owner decided to write authentication ourselves and not depend on an external auth service (no Supabase Auth, Auth0, Clerk or similar). Authentication is security-critical and the platform's value is trust, so the design must be simple, well tested and conventional.

## Options considered

### Option A: Opaque server-side sessions in PostgreSQL, sent as an httpOnly cookie

- Pros: easy to revoke (delete the row); nothing sensitive in the browser; no token-signing keys to rotate; fits a single backend and a browser frontend.
- Cons: one database lookup per request; cross-site cookie setup needs care (see Consequences).

### Option B: Stateless JWT access tokens plus refresh tokens

- Pros: no per-request lookup; usable by non-browser clients.
- Cons: revocation is hard; tokens in `localStorage` are exposed to XSS (the project forbids this); more moving parts to get wrong.

### Option C: An external auth service

- Pros: least code to write.
- Cons: rejected by the owner.

## Decision

Option A.

- Passwords are hashed with **argon2id** (`argon2-cffi`) with a per-user salt and parameters held in configuration. Rehash on login when parameters change.
- A login creates a session row: random 256-bit token, **stored only as a hash**, with user ID, created, last-seen, idle and absolute expiry, and user agent and IP for the audit log. The token is sent as a cookie that is `HttpOnly`, `Secure` and `SameSite` (value per the Consequences), with a `__Host-` prefix when the deployment allows it.
- State-changing requests are protected against CSRF (double-submit token or a required custom header, decided in B2.1), in addition to SameSite.
- Login is rate limited per account and per IP, uses generic error messages, and compares in constant time. Failed and successful logins, logouts and password changes go to the append-only audit log (B1.2).
- Roles (`ORG_ADMIN`, `WITNESS`, `PLATFORM_ADMIN`) are checked by a dependency on every protected route, with organisation scoping (B2.2). A test lists all routes and fails if one lacks a guard.
- Passwords, hashes and tokens never appear in logs or responses.

## Rationale

Server-side sessions give instant revocation and keep credentials out of JavaScript, which matches the spec's rule that tokens never live in `localStorage`. They are the least error-prone design for a first-party browser app.

## Consequences

- **Cross-origin cookies.** The frontend (Vercel) and the API (Railway) are different origins. Safari and other browsers block third-party cookies, so the API and the frontend must share a registrable domain (for example `amanah.example` and `api.amanah.example`, with `SameSite=Lax`), or the frontend must proxy `/api/*` to the API through a Next.js rewrite so the cookie is first-party. B12.1 and F0.6 must settle this before staging. Until then local development uses `localhost` for both.
- Writing auth ourselves means we own the review burden. B2.1 and B2.2 need the full test matrix in the roadmap and a security review before launch.
- Password reset (B2.4) stays P2.
- Follow-up: B2.1, B2.2, B2.3, B12.1, frontend F0.6 and F5.1.
