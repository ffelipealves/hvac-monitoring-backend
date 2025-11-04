from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional, Union

from monitoring_backend.application.dto.errors import ErrorResponseDTO
from monitoring_backend.application.usecases.usecase import UseCase


@dataclass
class UpdateCampusBodyDTO:
    name: Optional[str] = None

@dataclass
class UpdateCampusInputDTO:
    id: int
    name: Optional[str] = None


@dataclass
class UpdateCampusOutputDTO:
    id: int
    name: str

# Interface específica para o caso de uso
class IUpdateCampus(UseCase[UpdateCampusInputDTO, UpdateCampusOutputDTO]):
    @abstractmethod
    async def execute(self, input: UpdateCampusInputDTO) -> Union[UpdateCampusOutputDTO, ErrorResponseDTO]:
        ...
