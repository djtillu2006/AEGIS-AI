"""Carbon-data client boundary for future verified emissions providers."""


def get_emission_factor(mode: str) -> float:
    """Return an approximate starter factor in grams CO2 per ton-kilometre."""
    return {"sea": 15.0, "rail": 22.0, "air": 500.0}.get(mode, 15.0)
