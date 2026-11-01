# ADR-015: Modular monolith with enforced module boundaries

- **Status:** Accepted
- **Date:** 2026-11-01
- **Deciders:** Project owner (Haneef)
- **Related:** ADR-004 (backend stack), ADR-011 (authentication); BACKEND_ROADMAP B0.6, B1 to B10; spec §6 and §8

## Context

B0 left the API organised by technical layer: `app/api/` (routers), `app/schemas/` (models) and, from B1, one shared place for ORM models. Every feature from B1 to B10 would then touch all three folders, and nothing would stop one feature reaching into another's tables. The domain has clear areas with strict rules (the donation cap, the audit log, organisation scoping), and the deadline and team size rule out separate services. We want the code to be easy to navigate now and cheap to split later, without paying for a distributed system.

## Options considered

### Option A: keep the layered layout (`api/`, `schemas/`, `models/`, `services/`)

- Pros: nothing to change; familiar.
- Cons: a feature is spread over four folders; any code can import any table, so the cap and audit rules cannot be protected by structure; merge conflicts between unrelated features.

### Option B: modular monolith, one package per domain area, boundaries enforced by a test

- Pros: a feature lives in one folder; each module owns its tables and is the only code that writes them; cross-module calls go through a small, visible interface; one deployable unit, one database, one transaction (the donation cap needs that); a module can be extracted later because its dependencies are already explicit.
- Cons: some up-front structure; the boundary rule must be enforced or it erodes; cross-module reads need a deliberate interface instead of a quick join.

### Option C: separate services per area

- Pros: hard isolation.
- Cons: network calls and distributed transactions in the money path, several deployments to run on Railway, far more work than the deadline allows. Rejected.

## Decision

Adopt **Option B**.

```
app/
  main.py          wires every module's routers; the only place that knows all modules
  health.py        GET /health (system endpoint, not a business module)
  core/            config, logging, errors, error codes, request id, security scheme,
                   contract base types (schemas.py), stub helpers
  db/              declarative base, engine and session
  modules/
    auth/  organisations/  campaigns/  donations/  accountability/  audit/  admin/
      __init__.py   the public interface: `routers` plus the few names other modules may use
      router.py     HTTP endpoints
      schemas.py    request and response models
      models.py     ORM models; tables owned by this module alone
      service.py    business rules; the only code that touches this module's tables
```

Rules, enforced by `tests/architecture/test_module_boundaries.py` (a violation fails CI):

1. A module imports another module only through `app.modules.<name>` (its `__init__.py`). Importing `router`, `schemas`, `models` or `service` of another module is a violation.
2. Modules do not form import cycles.
3. `core` imports no other application code; `db` imports only `core`; no module imports `app.main`.
4. A module never reads or writes another module's tables. It calls that module's interface, which in B1 onwards means functions exported from its `__init__.py`.
5. Anything that is not one module's business (money and timestamp types, `ContractModel`, the error envelope) lives in `core`.

Where the 28 contract routes live:

| Module | Routes |
| ------ | ------ |
| `auth` | login, logout, current user |
| `organisations` | register an organisation |
| `campaigns` | public list and detail, public organisation profile (an organisation with its campaigns), the organisation dashboard's campaign list, create, edit, submit and close |
| `donations` | checkout, donation status, payment webhook |
| `accountability` | log expense, upload evidence, post update, assign witness, witness campaign list, witness confirmation |
| `admin` | the `/api/admin/*` back office: organisation verification, campaign review, excess handling, audit-log query. It calls the other modules' interfaces. |
| `audit` | no routes; owns the append-only log. The admin module exposes the query. |

The public organisation profile is served by `campaigns` because it is an organisation plus its campaigns. That keeps the dependency one-way (`campaigns` uses `organisations`, never the reverse).

The restructure changes no behaviour: `openapi.json` is byte-identical before and after.

## Rationale

The platform's trust story depends on a few rules being impossible to bypass: the cap is checked in one transaction, the audit log is append-only, organisations only see their own data. Giving each rule one owning module, and making the import rule a failing test, protects them better than convention. It also keeps the option to extract a module later without a rewrite, while staying a single deployment.

## Consequences

- Positive: features are easy to find and review; cross-module coupling is visible and tested; B1 onwards can add `models.py` and `service.py` per module.
- Negative or risks: the rule needs discipline for reads that span modules (use an interface function or a read model, not a join into foreign tables); shared Alembic metadata still lives in one `Base`, so every module's `models.py` must be imported in `migrations/env.py` (done through the module interfaces in B1.1).
- Follow-up work: B1.1 adds each module's `models.py`; B1.2 builds the `audit` module's write interface; add a CI note if a module is ever extracted.
