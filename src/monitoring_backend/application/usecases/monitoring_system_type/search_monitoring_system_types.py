from typing import List

from fastapi_pagination import Page
from dependency_injector.wiring import inject

from monitoring_backend.application.adapters.monitoring_system_type import MonitoringSystemTypePresenter
from monitoring_backend.application.repositories.monitoring_system_type import MonitoringSystemTypeRepository
from monitoring_backend.application.usecases.interfaces.monitoring_system_type.search_monitoring_system_type import (
    ISearchMonitoringSystemType,
    SearchMonitoringSystemTypeInputDTO,
)
from monitoring_backend.domain.entity.monitoring_system_type import MonitoringSystemType


class SearchMonitoringSystemType(ISearchMonitoringSystemType):
    """Caso de uso responsável por buscar e paginar tipos de sistemas de monitoramento."""

    @inject
    def __init__(self, monitoring_system_type_repository: MonitoringSystemTypeRepository):
        self.monitoring_system_type_repository = monitoring_system_type_repository

    async def execute(self, input_dto: SearchMonitoringSystemTypeInputDTO) -> Page:
        """Executa a busca paginada de tipos de sistema de monitoramento."""
        # Busca os tipos de sistema conforme filtros e paginação
        system_types, total = await self.monitoring_system_type_repository.search(
            input_dto.query_params,
            offset=(input_dto.pagination.page - 1) * input_dto.pagination.size,
            limit=input_dto.pagination.size,
        )

        # Caso não haja resultados, retorna uma página vazia
        if not system_types:
            return Page.create(items=[], total=0, params=input_dto.pagination)

        # Converte entidades para resposta JSON-friendly
        response = [
            MonitoringSystemTypePresenter.to_response(st) for st in system_types
        ]

        # Retorna a página paginada
        return Page.create(items=response, total=total, params=input_dto.pagination)
