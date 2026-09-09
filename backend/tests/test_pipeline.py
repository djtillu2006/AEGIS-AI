"""Integration test for the complete AEGIS AI pipeline."""

from api.pipeline import run_full_pipeline


def test_full_pipeline_returns_all_agent_outputs():
    result = run_full_pipeline("Rotterdam", "shipment-1", {"mode": "sea"}, {"max_extra_cost_pct": 200, "max_carbon_increase_pct": 200, "must_be_compliant": True}, "")
    assert set(result) >= {"risk_report", "scenarios", "route_plan", "compliance_report", "audit_result"}
    assert result["audit_result"]["audit_log_id"]
    assert result["auto_execution"] is False
