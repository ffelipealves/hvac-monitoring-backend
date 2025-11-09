from typing import List

from fastapi_pagination import Page
from dependency_injector.wiring import inject

from monitoring_backend.application.adapters.air_conditioner import AirConditionerPresenter
from monitoring_backend.application.repositories.air_conditioner import AirConditionerRepository
from monitoring_backend.application.usecases.interfaces.air_conditioner.search_air_conditioner import (
    ISearchAirConditioner,
    SearchAirConditionerInputDTO,
)
from monitoring_backend.domain.entity.air_conditioner import AirConditioner


class SearchAirConditioner(ISearchAirConditioner):
    """Caso de uso responsável por buscar e paginar ar-condicionados."""

    @inject
    def __init__(self, air_conditioner_repository: AirConditionerRepository):
        self.air_conditioner_repository = air_conditioner_repository

    async def execute(self, input: SearchAirConditionerInputDTO) -> Page:
        # Busca os ar condicionados com base nos filtros e paginação
        air_conditioners, total = await self.air_conditioner_repository.search(
            input.query_params,
            offset=(input.pagination.page - 1) * input.pagination.size,
            limit=input.pagination.size,
        )

        # Se não encontrar resultados, retorna página vazia
        if not air_conditioners:
            return Page.create(items=[], total=0, params=input.pagination)

        # Converte entidades para resposta JSON-friendly
        response = [
            AirConditionerPresenter.to_response(ac) for ac in air_conditioners
        ]

        # Cria a página paginada
        return Page.create(items=response, total=total, params=input.pagination)
