"""News API client boundary for future Reuters/Bloomberg integration."""


def fetch_headlines(port_name: str) -> list[dict]:
    """Return a provider-neutral headline response stub."""
    return [{"headline": f"Mock signal for {port_name}", "severity": 0.2}]
