"""Unit tests for the Digital Twin agent."""

from agents.digital_twin import DigitalTwinAgent, rank_scenarios
from models.port_risk import PortRiskReport


def test_scenarios_are_ranked_descending():
    risk = PortRiskReport(port_name="Rotterdam", psi_score=75, warning_window="12-36h")
    scenarios = DigitalTwinAgent().simulate("shipment-1", risk)
    assert scenarios == sorted(scenarios, key=lambda item: item["overall_score"], reverse=True)
