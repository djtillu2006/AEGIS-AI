"""AEGIS AI carbon and compliance report schema."""

from typing import Any

from pydantic import BaseModel, Field


class AegisComplianceReport(BaseModel):
    """Audit-ready carbon, regulatory, and policy findings for a route."""

    emissions: dict[str, Any] = Field(default_factory=dict)
    regulatory_findings: dict[str, Any] = Field(default_factory=dict)
    policy_findings: dict[str, Any] = Field(default_factory=dict)
