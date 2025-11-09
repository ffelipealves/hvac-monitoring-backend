from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict

from fastapi_pagination import Page, Params

from monitoring_backend.application.usecases.usecase import UseCase
from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit


@dataclass
class SearchMonitoringUnitInputDTO:
    """DTO de entrada para busca de unidades de monitoramento."""
    query_params: Dict[str, str]
    pagination: Params


class ISearchMonitoringUnit(UseCase[SearchMonitoringUnitInputDTO, Page[MonitoringUnit]]):
    """Interface (contrato) para o caso de uso de busca de unidades de monitoramento."""

    @abstractmethod
    async def execute(self, input: SearchMonitoringUnitInputDTO) -> Page[MonitoringUnit]:
        """Executa a busca de unidades de monitoramento com base nos parâmetros fornecidos."""
        ...
