"""Carrier quote client boundary for future freight marketplace integration."""


def request_quotes(mode: str, origin: str, destination: str) -> list[dict]:
    """Return provider-neutral carrier quote stubs."""
    return [{"carrier_name": f"Mock {mode} carrier", "origin": origin, "destination": destination, "availability": "pending"}]
