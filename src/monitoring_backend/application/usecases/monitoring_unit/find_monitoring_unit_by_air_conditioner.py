from dependency_injector.wiring import inject

from monitoring_backend.application.repositories.monitoring_unit import MonitoringUnitRepository
from monitoring_backend.application.usecases.interfaces.monitoring_unit.find_monitoring_unit_by_air_conditioner import (
    IFindMonitoringUnitByAirConditioner,
    FindMonitoringUnitByAirConditionerInputDTO,
)
from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit


class FindMonitoringUnitByAirConditioner(IFindMonitoringUnitByAirConditioner):
    """Caso de uso para buscar a unidade de monitoramento associada a um ar-condicionado."""

    @inject
    def __init__(self, monitoring_unit_repository: MonitoringUnitRepository):
        self.monitoring_unit_repository = monitoring_unit_repository

    async def execute(self, input: FindMonitoringUnitByAirConditionerInputDTO) -> MonitoringUnit | None:
        return await self.monitoring_unit_repository.find_by_air_conditioner(input.air_conditioner_id)
