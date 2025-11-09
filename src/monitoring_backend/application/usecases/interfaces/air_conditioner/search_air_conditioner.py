from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict

from fastapi_pagination import Page, Params

from monitoring_backend.application.usecases.usecase import UseCase
from monitoring_backend.domain.entity.air_conditioner import AirConditioner


@dataclass
class SearchAirConditionerInputDTO:
    """DTO de entrada para busca de ar-condicionados."""
    query_params: Dict[str, str]
    pagination: Params


class ISearchAirConditioner(UseCase[SearchAirConditionerInputDTO, Page[AirConditioner]]):
    """Interface (contrato) para o caso de uso de busca de ar-condicionados."""

    @abstractmethod
    async def execute(self, input: SearchAirConditionerInputDTO) -> Page[AirConditioner]:
        """Executa a busca de ar-condicionados com base nos parâmetros fornecidos."""
        ...
