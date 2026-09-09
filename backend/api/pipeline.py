"""End-to-end AEGIS AI orchestration flow."""

import logging
import time
from typing import Any

from agents.carbon_compliance import CarbonComplianceAgent
from agents.digital_twin import DigitalTwinAgent
from agents.market_sentinel import MarketSentinelAgent
from agents.orchestrator import OrchestratorAgent
from agents.trust_audit import TrustAuditAgent
from models.decision_chain import DecisionChain

logger = logging.getLogger(__name__)


def _run_step(name: str, action):
    """Run one pipeline step with structured timing logs."""
    started = time.perf_counter()
    logger.info("agent=%s input_summary=started", name)
    result = action()
    logger.info("agent=%s output_summary=%s duration_ms=%.2f", name, type(result).__name__, (time.perf_counter() - started) * 1000)
    return result


def run_full_pipeline(port_name: str, shipment_id: str, original_contract: dict, guardrails: dict, policy_doc_path: str) -> dict[str, Any]:
    """Run all five agents sequentially and return a human-gated combined result."""
    risk_report = _run_step("MarketSentinelAgent", lambda: MarketSentinelAgent().run(port_name))
    scenarios = _run_step("DigitalTwinAgent", lambda: DigitalTwinAgent().simulate(shipment_id, risk_report))
    chosen_scenario = scenarios[0]
    route_plan = _run_step("OrchestratorAgent", lambda: OrchestratorAgent().plan_and_negotiate(chosen_scenario, original_contract))
    compliance_report = _run_step("CarbonComplianceAgent", lambda: CarbonComplianceAgent().review(route_plan, policy_doc_path))
    chain = DecisionChain(risk_report=risk_report, scenarios=scenarios, chosen_scenario=chosen_scenario, route_plan=route_plan, compliance_report=compliance_report, agent_reasoning_steps=["Market signals and satellite findings were combined into PSI.", "Alternative scenarios were scored by cost, delay, and carbon.", "Carrier quotes were compared before route selection.", "Emissions and policy findings were recorded for audit."])
    audit_result = _run_step("TrustAuditAgent", lambda: TrustAuditAgent().review(chain, guardrails))
    return {"risk_report": risk_report.model_dump(mode="json"), "scenarios": scenarios, "route_plan": route_plan.model_dump(mode="json"), "compliance_report": compliance_report.model_dump(mode="json"), "audit_result": audit_result.model_dump(mode="json"), "human_approval_required": audit_result.requires_human_approval, "auto_execution": False}
