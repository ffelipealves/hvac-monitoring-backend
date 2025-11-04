from abc import abstractmethod
from dataclasses import dataclass

from monitoring_backend.application.usecases.usecase import UseCase

@dataclass
class CreateCampusInputDTO:
    name: str

@dataclass
class CreateCampusOutputDTO:
    id: str
    name: str

# Interface específica para o caso de uso
class ICreateCampus(UseCase[CreateCampusInputDTO, CreateCampusOutputDTO]):
    @abstractmethod
    async def execute(self, input: CreateCampusInputDTO) -> CreateCampusOutputDTO:
        ...
