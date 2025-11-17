from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


class MonitoringPayload(BaseModel):
    id: int | None = None
    monitoring_unit_id: int
    air_conditioner_id: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    temperature: float | None = None
    humidity: float | None = None
    power_consumption: float | None = None
    voltage: Optional[List[float]] = None
    current: Optional[List[float]] = None
    extra_data: dict | None = None
