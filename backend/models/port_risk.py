"""Schemas for port risk and Port Stress Index reports."""

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class PortRiskReport(BaseModel):
    """Audit-friendly risk report produced by the Market Sentinel agent."""

    port_name: str
    psi_score: float = Field(..., ge=0, le=100)
    warning_window: str
    top_signals: list[dict[str, Any]] = Field(default_factory=list)
    satellite_findings: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
