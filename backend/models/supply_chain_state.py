"""Schemas for the simulated supply-chain digital twin."""

from pydantic import BaseModel, Field


class ShipmentState(BaseModel):
    """Current operational values for one shipment."""

    shipment_id: str
    route: str
    current_cost: float = Field(ge=0)
    current_eta: str
    carbon_kg_co2: float = Field(ge=0)
    cargo_weight_tons: float = Field(default=1, gt=0)


class SupplyChainState(BaseModel):
    """Snapshot used as the input to scenario simulation."""

    shipment_id: str
    active_shipments: list[ShipmentState] = Field(default_factory=list)
    current_routes: list[str] = Field(default_factory=list)
    current_costs: dict[str, float] = Field(default_factory=dict)
    current_eta: dict[str, str] = Field(default_factory=dict)
    current_carbon_footprint: dict[str, float] = Field(default_factory=dict)
