"""FastAPI routes for the AEGIS AI five-agent architecture."""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from agents.carbon_compliance import CarbonComplianceAgent
from agents.digital_twin import DigitalTwinAgent
from agents.market_sentinel import MarketSentinelAgent
from agents.orchestrator import OrchestratorAgent
from agents.trust_audit import TrustAuditAgent
from api.pipeline import run_full_pipeline
from db.sqlite_store import approve_audit_log
from models.aegis_compliance_report import AegisComplianceReport
from models.decision_chain import AuditResult, DecisionChain
from models.port_risk import PortRiskReport
from models.route_plan import RoutePlan

router = APIRouter(prefix="/api", tags=["AEGIS AI Pipeline"])


class SimulationRequest(BaseModel):
    shipment_id: str
    risk_report: PortRiskReport
    num_scenarios: int = Field(default=3, ge=1, le=10)


class OrchestrationRequest(BaseModel):
    scenario: dict[str, Any]
    original_contract: dict[str, Any] = Field(default_factory=dict)


class ComplianceRequest(BaseModel):
    route: RoutePlan
    policy_doc_path: str = ""


class PipelineRequest(BaseModel):
    port_name: str
    shipment_id: str
    original_contract: dict[str, Any] = Field(default_factory=dict)
    guardrails: dict[str, Any] = Field(default_factory=lambda: {"max_extra_cost_pct": 100, "max_carbon_increase_pct": 100, "must_be_compliant": True})
    policy_doc_path: str = ""


class AuditRequest(BaseModel):
    chain: DecisionChain
    guardrails: dict[str, Any] = Field(default_factory=dict)


@router.post("/risk/{port_name}", response_model=PortRiskReport)
def assess_port_risk(port_name: str) -> PortRiskReport:
    """Run Market Sentinel for one port."""
    return MarketSentinelAgent().run(port_name)


@router.post("/simulate")
def simulate_supply_chain(request: SimulationRequest) -> list[dict[str, Any]]:
    """Run Digital Twin scenario simulation."""
    return DigitalTwinAgent().simulate(request.shipment_id, request.risk_report)[: request.num_scenarios]


@router.post("/orchestrate", response_model=RoutePlan)
def orchestrate_route(request: OrchestrationRequest) -> RoutePlan:
    """Convert a scenario into a quoted multimodal route plan."""
    return OrchestratorAgent().plan_and_negotiate(request.scenario, request.original_contract)


@router.post("/compliance", response_model=AegisComplianceReport)
def review_compliance(request: ComplianceRequest) -> AegisComplianceReport:
    """Review emissions, regulations, and company policy."""
    return CarbonComplianceAgent().review(request.route, request.policy_doc_path)


@router.post("/audit", response_model=AuditResult)
def audit_chain(request: AuditRequest) -> AuditResult:
    """Run the strict Trust & Audit gate."""
    return TrustAuditAgent().review(request.chain, request.guardrails)


@router.post("/pipeline/run")
def run_pipeline(request: PipelineRequest) -> dict[str, Any]:
    """Run all five agents and return a human-gated decision package."""
    return run_full_pipeline(request.port_name, request.shipment_id, request.original_contract, request.guardrails, request.policy_doc_path)


@router.post("/pipeline/approve/{audit_log_id}")
def approve_pipeline(audit_log_id: str) -> dict[str, Any]:
    """Record explicit human approval for an audited plan."""
    if not approve_audit_log(audit_log_id):
        raise HTTPException(status_code=404, detail="Audit log not found")
    return {"audit_log_id": audit_log_id, "approved": True, "auto_execution": False}
