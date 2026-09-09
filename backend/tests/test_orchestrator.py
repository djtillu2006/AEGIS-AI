"""Unit tests for the Logistics Orchestrator."""

from agents.orchestrator import OrchestratorAgent


def test_orchestrator_supports_multimodal_routes():
    route = OrchestratorAgent().plan_and_negotiate({"mode": "rail", "origin": "Delhi", "destination": "Mumbai", "total_cost": 5000, "delay_hours": 30}, {})
    assert route.mode == "rail"
    assert route.chosen_carrier
    assert route.contract_diff_summary
