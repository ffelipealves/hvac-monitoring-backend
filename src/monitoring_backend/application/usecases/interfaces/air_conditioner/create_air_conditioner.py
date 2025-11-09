from abc import abstractmethod
from dataclasses import dataclass

from monitoring_backend.application.usecases.usecase import UseCase
from monitoring_backend.domain.entity.air_conditioner import AirConditioner


@dataclass
class CreateAirConditionerInputDTO:
    """DTO de entrada para criação de um novo ar-condicionado."""
    name: str
    monitoring_unit_id: int  # unidade à qual será vinculado


class ICreateAirConditioner(UseCase[CreateAirConditionerInputDTO, AirConditioner]):
    """Interface para o caso de uso de criação de ar-condicionado."""

    @abstractmethod
    async def execute(self, input: CreateAirConditionerInputDTO) -> AirConditioner:
        """Cria um novo ar-condicionado e retorna a entidade criada."""
        ...
