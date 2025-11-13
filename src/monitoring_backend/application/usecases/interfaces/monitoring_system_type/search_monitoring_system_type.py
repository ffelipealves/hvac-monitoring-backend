from abc import ABC, abstractmethod
from typing import Dict
from fastapi_pagination import Params

from monitoring_backend.domain.entity.monitoring_system_type import MonitoringSystemType


class SearchMonitoringSystemTypeInputDTO:
    """DTO de entrada para busca paginada de tipos de sistema de monitoramento."""

    def __init__(self, query_params: Dict[str, str], pagination: Params):
        self.query_params = query_params
        self.pagination = pagination


class ISearchMonitoringSystemType(ABC):
    """Interface para caso de uso de busca de MonitoringSystemType."""

    @abstractmethod
    async def execute(self, input_dto: SearchMonitoringSystemTypeInputDTO):
        """Executa o caso de uso de busca de tipos de sistema de monitoramento."""
        pass
