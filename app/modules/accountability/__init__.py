"""Expenses, evidence, updates and witness confirmations. Interface of the accountability module."""

from fastapi import APIRouter

from app.modules.accountability.router import org_router, witness_router
from app.modules.accountability.schemas import (
    CampaignUpdate,
    EvidencePhoto,
    Expense,
    WitnessConfirmation,
    WitnessDecision,
)

routers: tuple[APIRouter, ...] = (
    org_router,
    witness_router,
)

__all__ = [
    "CampaignUpdate",
    "EvidencePhoto",
    "Expense",
    "WitnessConfirmation",
    "WitnessDecision",
    "routers",
]
