from dependency_injector.wiring import inject
from typing import List

from monitoring_backend.application.repositories.monitoring_unit import MonitoringUnitRepository
from monitoring_backend.application.usecases.interfaces.monitoring_unit.find_air_conditioners_by_monitoring_unit import (
    IFindAirConditionersByMonitoringUnit,
    FindAirConditionersByMonitoringUnitInputDTO,
)
from monitoring_backend.domain.entity.air_conditioner import AirConditioner


class FindAirConditionersByMonitoringUnit(IFindAirConditionersByMonitoringUnit):
    """Caso de uso para buscar todos os ar-condicionados de uma unidade de monitoramento."""

    @inject
    def __init__(self, monitoring_unit_repository: MonitoringUnitRepository):
        self.monitoring_unit_repository = monitoring_unit_repository

    async def execute(self, input: FindAirConditionersByMonitoringUnitInputDTO) -> List[AirConditioner]:
        monitoring_unit = await self.monitoring_unit_repository.get(input.monitoring_unit_id)
        if not monitoring_unit:
            raise ValueError(f"MonitoringUnit com id {input.monitoring_unit_id} não encontrada")

        return monitoring_unit.air_conditioners
