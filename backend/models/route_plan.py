"""Schemas for executable multimodal route plans."""

from typing import Literal

from pydantic import BaseModel, Field


class RoutePlan(BaseModel):
    """Concrete route proposal returned by the Logistics Orchestrator."""

    mode: Literal["sea", "air", "rail"]
    origin: str
    destination: str
    waypoints: list[str] = Field(default_factory=list)
    carrier_options: list[dict] = Field(default_factory=list)
    chosen_carrier: str | None = None
    estimated_cost: float = Field(ge=0)
    estimated_transit_time: float = Field(ge=0)
    distance_km: float = Field(default=1000, gt=0)
    cargo_weight_tons: float = Field(default=20, gt=0)
    contract_diff_summary: str = ""
