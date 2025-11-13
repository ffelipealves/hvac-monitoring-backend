from typing import Annotated, Dict, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi_pagination import Page, Params

from monitoring_backend.application.dto.errors import ErrorResponseDTO
from monitoring_backend.application.usecases.interfaces.monitoring_system_type.search_monitoring_system_type import (
    ISearchMonitoringSystemType,
    SearchMonitoringSystemTypeInputDTO,
)
# from monitoring_backend.application.usecases.interfaces.monitoring_system_type.create_monitoring_system_type import (
#     ICreateMonitoringSystemType,
#     CreateMonitoringSystemTypeInputDTO,
# )
# from monitoring_backend.application.usecases.interfaces.monitoring_system_type.find_by_unit import (
#     IFindMonitoringSystemTypeByUnit,
#     FindMonitoringSystemTypeByUnitInputDTO,
# )
from monitoring_backend.di import DependencyContainer


router = APIRouter(
    prefix="/monitoring-system-type",
    tags=["monitoring-system-type"],
)


# 🔍 Buscar (com paginação)
@router.get("/search", response_model=Page, responses={400: {"model": ErrorResponseDTO}})
@inject
async def search_monitoring_system_type(
    name: Optional[str] = Query(None, description="Filtrar por nome do tipo de sistema"),
    params: Params = Depends(),
    search_monitoring_system_type: ISearchMonitoringSystemType = Depends(
        Provide[DependencyContainer.search_monitoring_system_type]
    ),
):
    """Busca paginada de tipos de sistemas de monitoramento."""
    query_params: Dict[str, str] = {}
    if name is not None:
        query_params["name"] = name

    input_dto = SearchMonitoringSystemTypeInputDTO(query_params=query_params, pagination=params)
    result = await search_monitoring_system_type.execute(input_dto)
    return result


# ➕ Criar novo tipo de sistema
# @router.post(
#     "/",
#     responses={400: {"model": ErrorResponseDTO}},
# )
# @inject
# async def create_monitoring_system_type(
#     body: Annotated[
#         CreateMonitoringSystemTypeInputDTO,
#         Body(description="Dados para criação de um novo tipo de sistema de monitoramento"),
#     ],
#     create_monitoring_system_type: ICreateMonitoringSystemType = Depends(
#         Provide[DependencyContainer.create_monitoring_system_type]
#     ),
# ):
#     """Cria um novo tipo de sistema de monitoramento."""
#     return await create_monitoring_system_type.execute(body)


# # 🔎 Buscar tipo de sistema associado a uma unidade
# @router.get(
#     "/by-unit/{unit_id}",
#     responses={400: {"model": ErrorResponseDTO}},
# )
# @inject
# async def find_monitoring_system_type_by_unit(
#     unit_id: Annotated[int, Path(description="ID da unidade de monitoramento")],
#     find_by_unit: IFindMonitoringSystemTypeByUnit = Depends(
#         Provide[DependencyContainer.find_monitoring_system_type_by_unit]
#     ),
# ):
#     """Obtém o tipo de sistema associado a uma unidade de monitoramento."""
#     input_dto = FindMonitoringSystemTypeByUnitInputDTO(unit_id=unit_id)
#     result = await find_by_unit.execute(input_dto)
#     return result
