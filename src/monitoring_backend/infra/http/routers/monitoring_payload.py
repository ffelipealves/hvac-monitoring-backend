from typing import Annotated, Dict, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Query, Depends
from fastapi_pagination import Page, Params

from monitoring_backend.application.dto.errors import ErrorResponseDTO
from monitoring_backend.application.usecases.interfaces.monitoring_payload.search_monitoring_payload import (
    ISearchMonitoringPayload,
    SearchMonitoringPayloadInputDTO,
)
from monitoring_backend.di import DependencyContainer

router = APIRouter(
    prefix="/monitoring-payload",
    tags=["monitoring-payload"],
)

# 🔍 Buscar (com paginação e filtros opcionais)
@router.get("/search", response_model=Page, responses={400: {"model": ErrorResponseDTO}})
@inject
async def search_monitoring_payloads(
    monitoring_unit_id: Optional[int] = Query(None, description="Filtrar por ID da Monitoring Unit"),
    air_conditioner_id: Optional[int] = Query(None, description="Filtrar por ID do Air Conditioner"),
    params: Params = Depends(),
    search_monitoring_payload: ISearchMonitoringPayload = Depends(
        Provide[DependencyContainer.search_monitoring_payload]
    ),
):
    # Cria dicionário de filtros
    query_params: Dict[str, str] = {}
    if monitoring_unit_id is not None:
        query_params["monitoring_unit_id"] = str(monitoring_unit_id)
    if air_conditioner_id is not None:
        query_params["air_conditioner_id"] = str(air_conditioner_id)

    # Cria DTO de entrada
    input_dto = SearchMonitoringPayloadInputDTO(
        query_params=query_params,
        pagination=params,
    )

    # Executa caso de uso
    result = await search_monitoring_payload.execute(input_dto)
    return result
