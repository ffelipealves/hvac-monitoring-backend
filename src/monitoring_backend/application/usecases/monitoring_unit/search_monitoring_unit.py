from typing import List

from fastapi_pagination import Page
from dependency_injector.wiring import inject

from monitoring_backend.application.adapters.monitoring_unit import MonitoringUnitPresenter
from monitoring_backend.application.repositories.monitoring_unit import MonitoringUnitRepository
from monitoring_backend.application.usecases.interfaces.monitoring_unit.search_monitoring_unit import (
    ISearchMonitoringUnit,
    SearchMonitoringUnitInputDTO,
)
from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit


class SearchMonitoringUnit(ISearchMonitoringUnit):
    """Caso de uso responsável por buscar e paginar unidades de monitoramento."""

    @inject
    def __init__(self, monitoring_unit_repository: MonitoringUnitRepository):
        self.monitoring_unit_repository = monitoring_unit_repository

    async def execute(self, input: SearchMonitoringUnitInputDTO) -> Page:
        # Busca as unidades de monitoramento com base nos filtros e paginação
        monitoring_units, total = await self.monitoring_unit_repository.search(
            input.query_params,
            offset=(input.pagination.page - 1) * input.pagination.size,
            limit=input.pagination.size,
        )

        # Se não encontrar resultados, retorna página vazia
        if not monitoring_units:
            return Page.create(items=[], total=0, params=input.pagination)

        # Converte entidades para resposta JSON-friendly
        response = [
            MonitoringUnitPresenter.to_response(mu) for mu in monitoring_units
        ]

        # Cria a página paginada
        return Page.create(items=response, total=total, params=input.pagination)
