"""Schemas bundling the auditable AEGIS AI decision chain."""

from typing import Any

from pydantic import BaseModel, Field

from models.aegis_compliance_report import AegisComplianceReport
from models.port_risk import PortRiskReport
from models.route_plan import RoutePlan


class DecisionChain(BaseModel):
    """All inputs and outputs required for independent review."""

    risk_report: PortRiskReport
    scenarios: list[dict[str, Any]] = Field(default_factory=list)
    chosen_scenario: dict[str, Any]
    route_plan: RoutePlan
    compliance_report: AegisComplianceReport
    agent_reasoning_steps: list[str] = Field(default_factory=list)


class AuditResult(BaseModel):
    """Final gate result before a plan can be approved by a human."""

    approved: bool
    guardrail_results: dict[str, Any]
    hallucination_score: float = Field(ge=0, le=1)
    audit_log_id: str
    requires_human_approval: bool
    explanation: str = ""
