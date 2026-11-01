# Workflow: roadmap items, ADRs, changelog, commits

## 1. Roadmap item lifecycle

Files: `docs/roadmap/BACKEND_ROADMAP.md` (what and Definition of Done), `docs/roadmap/ROADMAP_INDEX.md` (**backend status — single source of truth**). The frontend roadmap is in https://github.com/haneefojay/amanah.

1. **Pick:** highest priority (P0 > P1 > P2) `Not started` item in the current milestone whose dependencies are `Done` or `Done (mocked)`. Never `Blocked` items; no P2 while a P0 in the milestone is open.
2. **Claim:** in the index status board set `In progress`, Owner, Updated (YYYY-MM-DD, Africa/Lagos).
3. **Build:** tests listed in the entry first where practical, then code. Stay inside the item's scope; new work found → new item with the next free ID (never renumber).
4. **Verify:** lint, type check and the full test suite (commands from B0.2).
5. **Close:** status `Done`; Notes = commit/PR link + anything notable; update "Current focus".
6. **Blocked:** status `Blocked`, reason in Notes, add a row to the index Blockers table, tell the user.
7. **Dropped:** status `Dropped` with the reason; keep the row.

Status values: `Not started`, `In progress`, `Done`, `Blocked`, `Dropped`. When a `B…` item changes status, tell the user so the frontend index mirror is updated.

## 2. ADRs (`docs/decisions/`)

Write one for any decision with lasting impact: a library, an architecture pattern, a resolved spec open decision (D1–D11), a deviation from the spec or roadmap.

1. Copy `docs/decisions/TEMPLATE.md` → `ADR-NNN-kebab-title.md` (next number across both repositories, three digits, never reused).
2. Fill every section: Context, **at least two** Options with pros/cons, Decision, Rationale, Consequences (with roadmap IDs). Status `Proposed` (awaiting the user) or `Accepted`; **always the date**.
3. Add a row to the index table in `docs/decisions/README.md`.
4. Changelog entry under **Decisions**.
5. Never edit an accepted ADR's decision; supersede it with a new ADR and mark the old one `Superseded by ADR-NNN`.

## 3. Changelog (`CHANGELOG.md`)

Every change gets an entry under `## [Unreleased]`, in the right section: Added, Changed, Fixed, Removed, Security, Decisions, Docs. Reference roadmap IDs and ADRs. One line per change, past tense, specific ("Added donate panel states (F4.1)", not "updates").

## 4. PROJECT_MEMORY.md

Update it in the same change when a durable fact changes (stack, conventions, owner instructions, open items). Keep it short; history goes to the changelog.

## 5. Git

- Branch per roadmap item: `feat/B6.1-checkout-reservations`, `fix/B7.3-webhook-replay`, `docs/…`, `chore/…`.
- Conventional commit subjects: `feat(B6.1): checkout with reservations`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`.
- **No AI attribution**: no `Co-Authored-By` lines for AI, no session trailers, no "Generated with …" in commits or PR descriptions. The author is the repository's configured git user (Ojutalayo Haneef Abiola).
- Never force-push or rewrite pushed history without the user's explicit request.
- Remote: `https://github.com/haneefojay/amanah-api` (branch `main`). CI must be green once B0.2 adds it.

## 6. When to stop and ask the user

- Any spec open decision beyond its default.
- New runtime dependency not covered by an ADR.
- Anything hard to reverse: deleting files or data, history rewrites, deployment changes, money/cap model changes.
- The spec and a roadmap entry disagree.
- Before large setup or architectural work: present suggestions and wait for the go-ahead (standing instruction from the owner).
