from abc import ABC, abstractmethod
from typing import Dict
from fastapi_pagination import Params

from monitoring_backend.domain.entity.monitoring_payload import MonitoringPayload


class SearchMonitoringPayloadInputDTO:
    """DTO de entrada para busca paginada de payloads."""

    def __init__(self, query_params: Dict[str, str], pagination: Params):
        self.query_params = query_params
        self.pagination = pagination


class ISearchMonitoringPayload(ABC):
    """Interface para caso de uso de busca de MonitoringPayload."""

    @abstractmethod
    async def execute(self, input: SearchMonitoringPayloadInputDTO):
        pass
