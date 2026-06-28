from datetime import datetime

from pydantic import BaseModel, Field


class Station(BaseModel):
    code: str
    name: str
    river: str
    department: str
    latitude: float | None = None
    longitude: float | None = None


class Observation(BaseModel):
    timestamp: datetime
    flow_m3s: float | None = Field(None, description="Discharge in m³/s")
    height_m: float | None = Field(None, description="Water height in metres")


class ObservationSeries(BaseModel):
    station: Station
    observations: list[Observation]
    period_hours: int
