"""Trust & Audit Agent for AEGIS AI."""

from datetime import datetime, timezone
import hashlib
import json
import uuid
from typing import Any

from db.sqlite_store import write_audit_log
from models.aegis_compliance_report import AegisComplianceReport
from models.decision_chain import AuditResult, DecisionChain


def enforce_guardrails(chain: DecisionChain, guardrails: dict[str, Any]) -> dict[str, Any]:
    """Evaluate hard cost, carbon, and compliance limits against the decision chain."""
    base_cost = float(chain.scenarios[0].get("total_cost", chain.route_plan.estimated_cost)) if chain.scenarios else chain.route_plan.estimated_cost
    max_cost_pct = float(guardrails.get("max_extra_cost_pct", 100))
    max_carbon_pct = float(guardrails.get("max_carbon_increase_pct", 100))
    baseline_carbon = float(chain.compliance_report.emissions.get("baseline_carbon_kg_co2", 8200))
    carbon = float(chain.compliance_report.emissions.get("carbon_kg_co2", 0))
    cost_pass = chain.route_plan.estimated_cost <= base_cost * (1 + max_cost_pct / 100)
    carbon_pass = carbon <= baseline_carbon * (1 + max_carbon_pct / 100)
    compliance_pass = not guardrails.get("must_be_compliant", True) or bool(chain.compliance_report.regulatory_findings.get("is_compliant", False))
    return {"max_extra_cost": {"passed": cost_pass, "actual_cost": chain.route_plan.estimated_cost, "baseline_cost": base_cost, "limit_pct": max_cost_pct}, "max_carbon_increase": {"passed": carbon_pass, "actual_carbon": carbon, "baseline_carbon": baseline_carbon, "limit_pct": max_carbon_pct}, "must_be_compliant": {"passed": compliance_pass}}


def score_hallucination_risk(chain: DecisionChain) -> float:
    """Return a conservative inconsistency score from reasoning and numeric outputs."""
    serialized = json.dumps(chain.model_dump(), default=str).lower()
    risk = 0.0
    if "guaranteed" in serialized or "certain" in serialized:
        risk += 0.25
    if not chain.route_plan.chosen_carrier:
        risk += 0.2
    if not chain.agent_reasoning_steps:
        risk += 0.2
    if chain.route_plan.estimated_cost <= 0 or chain.compliance_report.emissions.get("carbon_kg_co2", 0) < 0:
        risk += 0.4
    return min(1.0, round(risk, 3))


def generate_audit_log(chain: DecisionChain, guardrail_results: dict[str, Any], hallucination_score: float) -> dict[str, Any]:
    """Create and persist a tamper-evident audit record with a SHA-256 content hash."""
    audit_log_id = str(uuid.uuid4())
    record = {"audit_log_id": audit_log_id, "timestamp": datetime.now(timezone.utc).isoformat(), "status": "pending_human_review", "guardrail_results": guardrail_results, "hallucination_score": hallucination_score, "chain": chain.model_dump(mode="json")}
    record_hash = hashlib.sha256(json.dumps(record, sort_keys=True).encode("utf-8")).hexdigest()
    record["record_hash"] = record_hash
    write_audit_log(record)
    return record


class TrustAuditAgent:
    """Strict final approval gate for the AEGIS AI decision chain."""

    role = "Trust and Audit Reviewer"
    goal = "Independently validate guardrails, consistency, and traceability before human approval."
    backstory = "A skeptical assurance reviewer that never auto-executes a flagged plan."

    def review(self, chain: DecisionChain, guardrails: dict[str, Any]) -> AuditResult:
        """Run guardrails, score consistency, persist the audit record, and require review when needed."""
        results = enforce_guardrails(chain, guardrails)
        hallucination_score = score_hallucination_risk(chain)
        record = generate_audit_log(chain, results, hallucination_score)
        guardrails_passed = all(item.get("passed", False) for item in results.values())
        requires_human = (not guardrails_passed) or hallucination_score > 0.3
        return AuditResult(approved=False, guardrail_results=results, hallucination_score=hallucination_score, audit_log_id=record["audit_log_id"], requires_human_approval=requires_human, explanation="Human sign-off is required before execution." if requires_human else "Checks passed; human approval remains required by policy.")
