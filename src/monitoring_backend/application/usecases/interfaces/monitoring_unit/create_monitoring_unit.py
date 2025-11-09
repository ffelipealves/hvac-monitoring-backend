from abc import abstractmethod
from dataclasses import dataclass

from monitoring_backend.application.usecases.usecase import UseCase
from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit


@dataclass
class CreateMonitoringUnitInputDTO:
    """DTO de entrada para criação de uma unidade de monitoramento."""
    name: str
    campus_id: int


class ICreateMonitoringUnit(UseCase[CreateMonitoringUnitInputDTO, MonitoringUnit]):
    """Interface para o caso de uso de criação de uma unidade de monitoramento."""

    @abstractmethod
    async def execute(self, input: CreateMonitoringUnitInputDTO) -> MonitoringUnit:
        ...
