from abc import abstractmethod
from dataclasses import dataclass
from monitoring_backend.application.usecases.usecase import UseCase
from monitoring_backend.domain.entity.air_conditioner import AirConditioner


@dataclass
class UpdateAirConditionerInputDTO:
    """DTO de entrada para atualização de ar-condicionado."""
    id: int
    name: str


class IUpdateAirConditioner(UseCase[UpdateAirConditionerInputDTO, AirConditioner]):
    """Interface para o caso de uso de atualização de ar-condicionado."""

    @abstractmethod
    async def execute(self, input: UpdateAirConditionerInputDTO) -> AirConditioner:
        ...
