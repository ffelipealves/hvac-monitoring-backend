from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from monitoring_backend.application.usecases.usecase import UseCase
from monitoring_backend.domain.entity.air_conditioner import AirConditioner


@dataclass
class FindAirConditionersByMonitoringUnitInputDTO:
    """DTO para buscar todos os ar-condicionados de uma unidade de monitoramento."""
    monitoring_unit_id: int


class IFindAirConditionersByMonitoringUnit(
    UseCase[FindAirConditionersByMonitoringUnitInputDTO, List[AirConditioner]]
):
    """Interface para o caso de uso que lista todos os ar-condicionados de uma unidade de monitoramento."""

    @abstractmethod
    async def execute(
        self, input: FindAirConditionersByMonitoringUnitInputDTO
    ) -> List[AirConditioner]:
        ...
