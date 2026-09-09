"""Unit tests for the Market Sentinel agent."""

from agents.market_sentinel import analyze_satellite_image, calculate_psi, fetch_news_signals, MarketSentinelAgent


def test_market_sentinel_returns_structured_report():
    report = MarketSentinelAgent().run("Rotterdam")
    assert report.port_name == "Rotterdam"
    assert 0 <= report.psi_score <= 100
    assert report.satellite_findings["congestion_level"] in {"low", "medium", "high", "critical"}


def test_market_sentinel_mock_inputs_are_composable():
    signals = fetch_news_signals("Singapore")
    satellite = analyze_satellite_image("mock://singapore")
    result = calculate_psi(signals, satellite)
    assert "psi_score" in result
    assert "warning_window" in result
