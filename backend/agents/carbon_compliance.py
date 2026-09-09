"""Carbon & Compliance Co-Pilot for AEGIS AI."""

from pathlib import Path
from typing import Any
import json

from models.aegis_compliance_report import AegisComplianceReport
from models.route_plan import RoutePlan

# Approximate configurable grams CO2 per ton-kilometre factors.
EMISSION_FACTORS_G_PER_TON_KM = {"sea": 15.0, "rail": 22.0, "air": 500.0}


def calculate_emissions(route: RoutePlan) -> dict[str, Any]:
    """Estimate route emissions from mode, distance, and cargo weight inputs."""
    distance_km = float(getattr(route, "distance_km", 1000) or 1000)
    cargo_weight_tons = float(getattr(route, "cargo_weight_tons", 20) or 20)
    factor = EMISSION_FACTORS_G_PER_TON_KM[route.mode]
    carbon_kg = round(distance_km * cargo_weight_tons * factor / 1000, 2)
    return {"mode": route.mode, "distance_km": distance_km, "cargo_weight_tons": cargo_weight_tons, "emission_factor_g_per_ton_km": factor, "carbon_kg_co2": carbon_kg}


def _load_regulations() -> str:
    """Load local regulation summaries for deterministic, traceable review."""
    directory = Path(__file__).resolve().parent.parent / "data" / "regulations"
    texts = []
    for path in sorted(directory.glob("*.txt")):
        texts.append(f"## {path.name}\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(texts)


def check_compliance(route: RoutePlan, emissions: dict[str, Any]) -> dict[str, Any]:
    """Check emissions against local regulation summaries and return traceable findings."""
    regulations = _load_regulations()
    carbon = float(emissions["carbon_kg_co2"])
    return {"is_compliant": carbon <= 10000, "flagged_issues": ["High-emission transport mode" ] if carbon > 10000 else [], "required_disclosures": ["Route mode", "Distance and cargo weight", "Emission factor", "Regulation summaries consulted"], "regulation_context_length": len(regulations)}


def check_company_policy(route: RoutePlan, emissions: dict[str, Any], policy_doc_path: str) -> dict[str, Any]:
    """Check a route against a local policy document, falling back to a 12,000 kg limit."""
    max_carbon = 12000.0
    path = Path(policy_doc_path)
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        for token in text.replace("=", " ").split():
            try:
                if "carbon" in token.lower():
                    max_carbon = float(next(value for value in text.replace("=", " ").split() if value.replace(".", "", 1).isdigit()))
                    break
            except (StopIteration, ValueError):
                pass
    carbon = float(emissions["carbon_kg_co2"])
    return {"policy_compliant": carbon <= max_carbon, "violations": [] if carbon <= max_carbon else [f"Carbon {carbon} kg exceeds policy limit {max_carbon} kg"], "max_carbon_kg_co2": max_carbon}


class CarbonComplianceAgent:
    """CrewAI-compatible carbon and regulatory review facade."""

    role = "Carbon and Compliance Co-Pilot"
    goal = "Produce traceable emissions and policy findings for every route plan."
    backstory = "An audit-minded ESG analyst who cites input data and regulation summaries."

    def review(self, route: RoutePlan, policy_doc_path: str = "") -> AegisComplianceReport:
        """Calculate emissions and combine regulatory and policy findings."""
        emissions = calculate_emissions(route)
        regulatory = check_compliance(route, emissions)
        policy = check_company_policy(route, emissions, policy_doc_path)
        return AegisComplianceReport(emissions=emissions, regulatory_findings=regulatory, policy_findings=policy)
