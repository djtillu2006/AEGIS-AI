"""Logistics Orchestrator + Negotiator agent for AEGIS AI."""

from typing import Any
import logging

from models.route_plan import RoutePlan

logger = logging.getLogger(__name__)


def build_route(scenario: dict[str, Any]) -> RoutePlan:
    """Convert a ranked digital-twin scenario into a multimodal route plan."""
    mode = str(scenario.get("mode", "sea")).lower()
    if mode not in {"sea", "air", "rail"}:
        mode = "sea"
    return RoutePlan(
        mode=mode,
        origin=str(scenario.get("origin", "Shanghai")),
        destination=str(scenario.get("destination", "Rotterdam")),
        waypoints=list(scenario.get("waypoints", ["Singapore"] if mode == "sea" else [])),
        estimated_cost=float(scenario.get("total_cost", 15000)),
        estimated_transit_time=float(scenario.get("delay_hours", 72)),
        distance_km=float(scenario.get("distance_km", 1000)),
        cargo_weight_tons=float(scenario.get("cargo_weight_tons", 20)),
    )


def request_carrier_quotes(route: RoutePlan) -> list[dict[str, Any]]:
    """Return carrier quote stubs that can later be replaced by marketplace clients."""
    multiplier = {"sea": 1.0, "rail": 1.35, "air": 2.5}[route.mode]
    return [
        {"carrier_name": f"AEGIS {route.mode.title()} Partner", "cost": round(route.estimated_cost * multiplier, 2), "transit_time": route.estimated_transit_time, "availability": "confirmed"},
        {"carrier_name": f"Alternative {route.mode.title()} Carrier", "cost": round(route.estimated_cost * multiplier * 1.08, 2), "transit_time": max(12, route.estimated_transit_time - 12), "availability": "pending"},
    ]


def select_best_quote(quotes: list[dict[str, Any]]) -> dict[str, Any]:
    """Select a quote using a configurable 60% cost and 40% speed preference."""
    if not quotes:
        raise ValueError("At least one carrier quote is required")
    max_cost = max(float(quote["cost"]) for quote in quotes)
    max_time = max(float(quote["transit_time"]) for quote in quotes)
    return min(quotes, key=lambda quote: 0.6 * float(quote["cost"]) / max_cost + 0.4 * float(quote["transit_time"]) / max_time)


def draft_contract_changes(original_contract: dict[str, Any], new_route: RoutePlan) -> str:
    """Draft a plain-language contract delta, with Gemini available as a future provider."""
    original_mode = original_contract.get("mode", "existing")
    return f"Update mode from {original_mode} to {new_route.mode}; revise carrier, waypoints, cost, and transit-time clauses for the proposed route."


class OrchestratorAgent:
    """CrewAI-compatible route planning and carrier negotiation facade."""

    role = "Logistics Orchestrator and Negotiator"
    goal = "Turn the best scenario into a concrete, quoted multimodal route plan."
    backstory = "A pragmatic logistics planner who compares sea, air, and rail capacity."

    def plan_and_negotiate(self, scenario: dict[str, Any], original_contract: dict[str, Any]) -> RoutePlan:
        """Build a route, collect quotes, choose one, and draft contract changes."""
        route = build_route(scenario)
        quotes = request_carrier_quotes(route)
        selected = select_best_quote(quotes)
        route = route.model_copy(update={
            "carrier_options": quotes,
            "chosen_carrier": selected["carrier_name"],
            "estimated_cost": float(selected["cost"]),
            "estimated_transit_time": float(selected["transit_time"]),
            "contract_diff_summary": draft_contract_changes(original_contract, route),
        })
        return route
