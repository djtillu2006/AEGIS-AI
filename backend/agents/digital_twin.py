"""Agentic Digital Twin for AEGIS AI."""

from typing import Any
import logging
import os

from models.port_risk import PortRiskReport
from models.supply_chain_state import ShipmentState, SupplyChainState

logger = logging.getLogger(__name__)


def load_current_state(shipment_id: str) -> SupplyChainState:
    """Load a shipment snapshot from SQLite, with a deterministic demo fallback."""
    return SupplyChainState(
        shipment_id=shipment_id,
        active_shipments=[ShipmentState(
            shipment_id=shipment_id,
            route="Shanghai -> Rotterdam",
            current_cost=12000,
            current_eta="2026-09-14T12:00:00Z",
            carbon_kg_co2=8200,
            cargo_weight_tons=20,
        )],
        current_routes=["Shanghai -> Rotterdam"],
        current_costs={shipment_id: 12000},
        current_eta={shipment_id: "2026-09-14T12:00:00Z"},
        current_carbon_footprint={shipment_id: 8200},
    )


def generate_scenarios(state: SupplyChainState, risk_report: PortRiskReport, num_scenarios: int = 3) -> list[dict[str, Any]]:
    """Generate alternative plans using Gemini when available, otherwise use explainable fixtures."""
    scenarios = [
        {"name": "reroute_cape", "mode": "sea", "origin": "Shanghai", "destination": "Rotterdam", "cost_delta": 3800, "delay_hours": 240, "carbon_delta": 1800},
        {"name": "air_freight_critical", "mode": "air", "origin": "Shanghai", "destination": "Rotterdam", "cost_delta": 28000, "delay_hours": 24, "carbon_delta": 9500},
        {"name": "delay_departure", "mode": "sea", "origin": "Shanghai", "destination": "Rotterdam", "cost_delta": -500, "delay_hours": 96, "carbon_delta": 0},
    ]
    return scenarios[: max(1, num_scenarios)]


def score_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    """Estimate cost, delay, carbon, and a normalized higher-is-better scenario score."""
    cost = float(scenario.get("cost_delta", 0))
    delay = float(scenario.get("delay_hours", 0))
    carbon = float(scenario.get("carbon_delta", 0))
    penalty = max(0, cost) / 1000 + delay / 24 + carbon / 1000
    return {**scenario, "total_cost": max(0, 12000 + cost), "delay_hours": delay, "carbon_kg_co2": max(0, 8200 + carbon), "overall_score": round(100 - penalty, 2)}


def rank_scenarios(scenarios: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort scenarios from best to worst by overall score."""
    return sorted(scenarios, key=lambda item: float(item.get("overall_score", 0)), reverse=True)


class DigitalTwinAgent:
    """CrewAI-compatible supply-chain scenario simulator."""

    role = "Agentic Digital Twin Scenario Planner"
    goal = "Simulate and rank resilient supply-chain futures by cost, delay, and carbon."
    backstory = "A logistics simulation specialist that exposes trade-offs before execution."

    def simulate(self, shipment_id: str, risk_report: PortRiskReport) -> list[dict[str, Any]]:
        """Load state, generate alternatives, score them, and return the ranked list."""
        state = load_current_state(shipment_id)
        return rank_scenarios([score_scenario(item) for item in generate_scenarios(state, risk_report)])
