"""Unit tests for the Trust & Audit Agent."""

from agents.trust_audit import TrustAuditAgent
from models.aegis_compliance_report import AegisComplianceReport
from models.decision_chain import DecisionChain
from models.port_risk import PortRiskReport
from models.route_plan import RoutePlan


def test_failed_guardrail_requires_human_approval():
    chain = DecisionChain(
        risk_report=PortRiskReport(port_name="Rotterdam", psi_score=60, warning_window="24-72h"),
        scenarios=[{"total_cost": 1000}],
        chosen_scenario={"total_cost": 1000},
        route_plan=RoutePlan(mode="air", origin="A", destination="B", estimated_cost=10000, estimated_transit_time=10),
        compliance_report=AegisComplianceReport(emissions={"carbon_kg_co2": 20000}, regulatory_findings={"is_compliant": False}),
        agent_reasoning_steps=["reviewed"],
    )
    result = TrustAuditAgent().review(chain, {"max_extra_cost_pct": 10, "max_carbon_increase_pct": 10, "must_be_compliant": True})
    assert result.requires_human_approval is True
