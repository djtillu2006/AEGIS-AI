"""Unit tests for the Carbon & Compliance Co-Pilot."""

from agents.carbon_compliance import CarbonComplianceAgent
from models.route_plan import RoutePlan


def test_compliance_report_contains_traceable_emissions():
    route = RoutePlan(mode="sea", origin="Shanghai", destination="Rotterdam", estimated_cost=10000, estimated_transit_time=240)
    report = CarbonComplianceAgent().review(route)
    assert "carbon_kg_co2" in report.emissions
    assert "is_compliant" in report.regulatory_findings
    assert "policy_compliant" in report.policy_findings
