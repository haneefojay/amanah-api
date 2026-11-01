# ADR-013: Object storage on MinIO behind an S3-compatible adapter

- **Status:** Accepted
- **Date:** 2026-11-01
- **Deciders:** Project owner (Haneef)
- **Related:** spec §7, §9; BACKEND_ROADMAP B3.2, B8.1, B8.2; ADR-012

## Context

The platform stores receipts, evidence photos, organisation verification documents and update photos. Verification documents are private; published evidence and receipts are public. The owner chose MinIO.

## Options considered

### Option A: MinIO, accessed through the S3 API

- Pros: self-hosted and S3-compatible, so it runs on Railway now and on a VPS later and works the same locally in Docker Compose; no vendor lock-in.
- Cons: we operate it (volume, backups, upgrades); browsers must reach it for signed URLs.

### Option B: A hosted service (Cloudflare R2, AWS S3, Supabase Storage)

- Pros: no storage server to run.
- Cons: not what the owner chose; an extra vendor.

## Decision

Option A. The API talks to storage only through a small **storage adapter** using the S3 API (`boto3` or `aioboto3`), so MinIO can later be swapped for R2 or S3 by configuration.

- Two buckets: `public` (receipts, published evidence, update photos) and `private` (verification documents). Private objects are served only through short-lived signed URLs.
- Uploads use signed URLs or a multipart endpoint, with content-type and size validation, image-only for evidence, and object keys that do not use the user's file name.
- Storage credentials stay on the server and never reach the client (B8.1). Configuration comes from environment variables.
- The public MinIO endpoint must be reachable by browsers for signed URLs and public reads. Data lives on a persistent volume with backups.

## Rationale

The S3 API is the stable interface; MinIO is a portable way to meet it that fits the Railway-then-VPS plan.

## Consequences

- Positive: same storage locally, on staging and later on a VPS.
- Negative or risks: operating MinIO ourselves; backup and restore must be tested (B12.4). If this becomes a burden, switch the adapter to a hosted S3-compatible service with a new ADR.
- Follow-up: B8.1, B8.2, B3.2, B12.4, B0.4 (MinIO in Docker Compose).
