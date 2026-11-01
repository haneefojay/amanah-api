"""Audit log models (B1.2, B10.4)."""

from uuid import UUID

from app.core.schemas import (
    ContractModel,
    Text,
    Timestamp,
)


class AuditEntry(ContractModel):
    id: UUID
    actor_id: UUID | None
    action: Text
    entity_type: Text
    entity_id: UUID | None
    payload: dict[str, object]
    created_at: Timestamp


class AuditLogResponse(ContractModel):
    data: list[AuditEntry]
