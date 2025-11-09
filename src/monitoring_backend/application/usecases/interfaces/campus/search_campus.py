from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict

from monitoring_backend.application.usecases.usecase import UseCase
from monitoring_backend.domain.entity.campus import Campus

from fastapi_pagination import Page, Params

@dataclass
class SearchCampusInputDTO:
    query_params: Dict[str, str]
    pagination: Params

# Interface específica para o caso de uso
class ISearchCampus(UseCase[SearchCampusInputDTO, None]):
    @abstractmethod
    async def execute(self, input: SearchCampusInputDTO) -> Page:
        ...
