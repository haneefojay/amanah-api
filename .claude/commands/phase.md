---
description: Start a backend roadmap phase or item (e.g. /phase B2 or /phase B2.1). Reads the project rules, plans, asks questions, and waits for approval before building.
argument-hint: <B<n> | B<n>.<m>>
---

# /phase $ARGUMENTS

You are starting work on backend roadmap **$ARGUMENTS** for Amanah API. This is a fresh session, so build your context from the repository files below before anything else.

Three stages: **1. Read**, **2. Plan and ask**, **3. Build after approval**. Do not skip or merge them. You must not edit any file, install anything, change roadmap status, or commit until the owner has approved the plan in stage 2.

---

## 0. Check the argument

- Valid forms: `B<n>` (a whole phase, e.g. `B2`) and `B<n>.<m>` (one item, e.g. `B2.1`). `F…` items belong to the frontend repository (https://github.com/haneefojay/amanah); say so and stop.
- If `$ARGUMENTS` is empty or invalid, stop and ask which phase or item to start.

## 1. Read (no edits yet)

1. `CLAUDE.md` and `AGENTS.md`.
2. The `amanah-api` skill: `.claude/skills/amanah-api/SKILL.md` and its references (`domain-rules.md`, `workflow.md`).
3. `PROJECT.md` and `docs/architecture.md`.
4. `docs/roadmap/ROADMAP_INDEX.md`: current focus, status board, blockers, open decisions.
5. `docs/roadmap/BACKEND_ROADMAP.md`: "How to read", the Global Definition of Done, and the full entry of every item in scope and of the items they depend on. Also the cross-reference table at the end, and the matching `F…` entries in the frontend roadmap.
6. The spec sections the items cite, plus §1 (scope), §4 (the cap), §9 (non-functional) and §11 (open decisions).
7. `docs/decisions/README.md` and the related ADRs (always ADR-003, ADR-004, ADR-011 for auth work, ADR-012 for deployment, ADR-013 for files).
8. The latest `CHANGELOG.md` entries and the code that already exists for this area.

Check the status board: skip `Done` items, flag `Blocked` ones or those with unfinished dependencies, and ask before taking over an item that is `In progress` under someone else.

## 2. Plan and ask (then STOP and wait)

Present, concretely and skimmably:

1. **Scope:** items in build order with ID, title and priority; what is excluded and why.
2. **Per item:** files to create or change, endpoints (method, path, request and response shapes, error codes), database changes and migrations, tests from the roadmap entry (unit, integration against real PostgreSQL, concurrency where relevant), and how its Definition of Done is met.
3. **Contract impact:** every new or changed API shape, and which frontend items and mock handlers must follow.
4. **Risks and decisions:** open spec decisions (D1 to D11), any new dependency (needs an ADR), anything hard to reverse, spec-versus-roadmap conflicts, anything that threatens the deadline. Give a recommended default for each.
5. **Questions:** only what you need, numbered, ideally multiple choice with a recommendation.
6. **Delivery:** how the work splits into branches and commits, and how it will be verified.

Then **stop and wait** for explicit approval.

## 3. Build (only after approval)

For each item in order:

1. Claim it in `docs/roadmap/ROADMAP_INDEX.md` (`In progress`, owner, date).
2. Tests first where practical, then code, inside the item's scope. New work found gets a new roadmap ID (never renumber).
3. Follow every hard rule in the `amanah-api` skill.
4. Run lint, type check and the full tests. Fix failures; never weaken a test to pass.
5. Close the item (`Done`), add notes, update "Current focus", add a `CHANGELOG.md` entry, regenerate OpenAPI if endpoints changed, write an ADR for lasting decisions, and update `CLAUDE.md` if a durable fact changed.
6. Commit as the configured git user with **no AI attribution**.
7. Stop and ask the owner whenever AGENTS.md §6 applies, even mid-build.

When everything in scope is done, report what was built (item by item with final status), what was tested, what remains or is blocked, decisions the owner needs to make, and which frontend items must follow.
