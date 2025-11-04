from abc import abstractmethod
from dataclasses import dataclass

from monitoring_backend.application.usecases.usecase import UseCase

@dataclass
class GetCampusByIdInputDTO:
    id: int

@dataclass
class GetCampusByIdOutputDTO:
    id: str
    name: str


# Interface específica para o caso de uso
class IGetCampusById(UseCase[GetCampusByIdInputDTO, GetCampusByIdOutputDTO]):
    @abstractmethod
    async def execute(self, input: GetCampusByIdInputDTO) -> GetCampusByIdOutputDTO:
        ...
