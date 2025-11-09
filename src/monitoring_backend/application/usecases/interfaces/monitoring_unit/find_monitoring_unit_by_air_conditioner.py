from abc import abstractmethod
from dataclasses import dataclass
from monitoring_backend.application.usecases.usecase import UseCase
from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit


@dataclass
class FindMonitoringUnitByAirConditionerInputDTO:
    """DTO para buscar a unidade de monitoramento de um ar-condicionado."""
    air_conditioner_id: int


class IFindMonitoringUnitByAirConditioner(
    UseCase[FindMonitoringUnitByAirConditionerInputDTO, MonitoringUnit]
):
    """Interface para o caso de uso de busca da unidade de monitoramento por ar-condicionado."""

    @abstractmethod
    async def execute(
        self, input: FindMonitoringUnitByAirConditionerInputDTO
    ) -> MonitoringUnit:
        ...
