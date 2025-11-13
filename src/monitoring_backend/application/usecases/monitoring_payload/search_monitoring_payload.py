from typing import Dict
from fastapi_pagination import Page
from dependency_injector.wiring import inject

from monitoring_backend.application.adapters.monitoring_payload import MonitoringPayloadPresenter
from monitoring_backend.application.repositories.monitoring_payload import MonitoringPayloadRepository
from monitoring_backend.application.usecases.interfaces.monitoring_payload.search_monitoring_payload import (
    ISearchMonitoringPayload,
    SearchMonitoringPayloadInputDTO,
)
from monitoring_backend.domain.entity.monitoring_payload import MonitoringPayload


class SearchMonitoringPayload(ISearchMonitoringPayload):
    """Caso de uso responsável por buscar e paginar dados de monitoramento."""

    @inject
    def __init__(self, monitoring_payload_repository: MonitoringPayloadRepository):
        self.monitoring_payload_repository = monitoring_payload_repository

    async def execute(self, input: SearchMonitoringPayloadInputDTO) -> Page:
        """Executa a busca e retorna os payloads paginados."""
        payloads, total = await self.monitoring_payload_repository.search(
            input.query_params,
            offset=(input.pagination.page - 1) * input.pagination.size,
            limit=input.pagination.size,
        )

        if not payloads:
            return Page.create(items=[], total=0, params=input.pagination)

        response = [MonitoringPayloadPresenter.to_response(p) for p in payloads]

        return Page.create(items=response, total=total, params=input.pagination)
