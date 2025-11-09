# from abc import abstractmethod
# from dataclasses import dataclass
# from monitoring_backend.application.usecases.usecase import UseCase
# from monitoring_backend.domain.entity.air_conditioner import AirConditioner


# @dataclass
# class GetAirConditionerInputDTO:
#     """DTO de entrada para busca de ar-condicionado por ID."""
#     id: int


# class IGetAirConditioner(UseCase[GetAirConditionerInputDTO, AirConditioner]):
#     """Interface para o caso de uso de busca de ar-condicionado por ID."""

#     @abstractmethod
#     async def execute(self, input: GetAirConditionerInputDTO) -> AirConditioner:
#         ...
