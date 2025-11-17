from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, List

from monitoring_backend.application.usecases.usecase import UseCase


# ===============================
# 📥 DTO de Entrada
# ===============================
@dataclass
class CreateMonitoringPayloadInputDTO:
    monitoring_unit_id: int
    air_conditioner_id: int
    timestamp: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    power_consuption: Optional[float] = None
    voltage: Optional[List[float]] = None
    current: Optional[List[float]] = None
    extra_data: Optional[dict] = None


# ===============================
# 📤 DTO de Saída
# ===============================
@dataclass
class CreateMonitoringPayloadOutputDTO:
    id: int
    monitoring_unit_id: int
    air_conditioner_id: int
    timestamp: str
    temperature: Optional[float]
    humidity: Optional[float]
    voltage: Optional[List[float]]
    current: Optional[List[float]]
    extra_data: Optional[dict]


# ===============================
# 🔌 Interface do UseCase
# ===============================
class ICreateMonitoringPayload(
    UseCase[
        CreateMonitoringPayloadInputDTO,
        CreateMonitoringPayloadOutputDTO
    ]
):
    @abstractmethod
    async def execute(
        self,
        input: CreateMonitoringPayloadInputDTO
    ) -> CreateMonitoringPayloadOutputDTO:
        ...
