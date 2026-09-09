"""Market Sentinel + Satellite PSI agent for AEGIS AI."""

from datetime import datetime, timezone
from typing import Any
import json
import logging
import os
import re

from models.port_risk import PortRiskReport

logger = logging.getLogger(__name__)


def fetch_news_signals(port_name: str) -> list[dict[str, Any]]:
    """Return relevant news risk signals, using deterministic data until a news API is configured."""
    normalized = port_name.lower()
    if "rotterdam" in normalized or "suez" in normalized:
        return [{
            "headline": f"Elevated congestion and disruption risk near {port_name}",
            "source": "AEGIS mock news feed",
            "severity": 0.75,
            "sentiment": -0.65,
        }]
    return [{
        "headline": f"Routine operations reported for {port_name}",
        "source": "AEGIS mock news feed",
        "severity": 0.15,
        "sentiment": 0.1,
    }]


def analyze_satellite_image(image_url_or_path: str) -> dict[str, Any]:
    """Analyze satellite imagery with Gemini when configured, otherwise return a mock finding."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key and image_url_or_path.startswith(("http://", "https://")):
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(os.getenv("GEMINI_VISION_MODEL", "gemini-1.5-flash"))
            response = model.generate_content(
                ["Return JSON with congestion_level, estimated_vessel_count, visible_anomalies.", image_url_or_path]
            )
            text = getattr(response, "text", "")
            parsed = json.loads(re.search(r"\{.*\}", text, re.DOTALL).group(0))
            return parsed
        except Exception as exc:
            logger.warning("Gemini satellite analysis unavailable: %s", exc)
    return {
        "congestion_level": "medium",
        "estimated_vessel_count": 24,
        "visible_anomalies": ["unusual vessel clustering"],
    }


def calculate_psi(news_signals: list[dict[str, Any]], satellite_analysis: dict[str, Any]) -> dict[str, Any]:
    """Combine news severity and satellite congestion into a 0-100 Port Stress Index."""
    news_score = max((float(signal.get("severity", 0)) for signal in news_signals), default=0)
    congestion_scores = {"low": 10, "medium": 40, "high": 70, "critical": 95}
    satellite_score = congestion_scores.get(str(satellite_analysis.get("congestion_level", "low")).lower(), 40)
    score = round(min(100, news_score * 45 + satellite_score * 0.55), 2)
    if score >= 75:
        warning_window = "delay likely in 12-36h"
    elif score >= 45:
        warning_window = "delay possible in 24-72h"
    else:
        warning_window = "no material delay expected in 72h"
    return {"psi_score": score, "warning_window": warning_window}


class MarketSentinelAgent:
    """CrewAI-compatible agent facade for port news and satellite risk analysis."""

    role = "Market Sentinel and Satellite Port Stress Analyst"
    goal = "Detect early port disruption signals and quantify the Port Stress Index."
    backstory = "An independent maritime intelligence analyst who combines open signals with imagery."

    def run(self, port_name: str) -> PortRiskReport:
        """Run news collection, satellite analysis, and PSI calculation for a port."""
        signals = fetch_news_signals(port_name)
        satellite = analyze_satellite_image(f"mock://{port_name}")
        psi = calculate_psi(signals, satellite)
        return PortRiskReport(
            port_name=port_name,
            psi_score=psi["psi_score"],
            warning_window=psi["warning_window"],
            top_signals=signals,
            satellite_findings=satellite,
            timestamp=datetime.now(timezone.utc),
        )
