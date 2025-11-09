from typing import Annotated, Dict, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi_pagination import Page, Params

from monitoring_backend.application.dto.errors import ErrorResponseDTO
from monitoring_backend.application.usecases.interfaces.monitoring_unit.create_monitoring_unit import (
    ICreateMonitoringUnit,
    CreateMonitoringUnitInputDTO,
)
# from monitoring_backend.application.usecases.interfaces.monitoring_unit.get_monitoring_unit_by_id import (
#     IGetMonitoringUnitById,
#     GetMonitoringUnitByIdInputDTO,
# )
from monitoring_backend.application.usecases.interfaces.monitoring_unit.search_monitoring_unit import (
    ISearchMonitoringUnit,
    SearchMonitoringUnitInputDTO,
)

# from monitoring_backend.application.usecases.interfaces.monitoring_unit.update_monitoring_unit import (
#     IUpdateMonitoringUnit,
#     UpdateMonitoringUnitInputDTO,
#     UpdateMonitoringUnitBodyDTO,
# )
# from monitoring_backend.application.usecases.interfaces.monitoring_unit.delete_monitoring_unit import (
#     IDeleteMonitoringUnit,
#     DeleteMonitoringUnitInputDTO,
# )

from monitoring_backend.application.usecases.interfaces.monitoring_unit.find_air_conditioners_by_monitoring_unit import (
    IFindAirConditionersByMonitoringUnit,
    FindAirConditionersByMonitoringUnitInputDTO,
)
from monitoring_backend.di import DependencyContainer


router = APIRouter(
    prefix="/monitoring-unit",
    tags=["monitoring-unit"],
)


# 🔍 Buscar (com paginação)
@router.get("/search", response_model=Page, responses={400: {"model": ErrorResponseDTO}})
@inject
async def search_monitoring_unit(
    name: Optional[str] = Query(None, description="Filtrar por nome da unidade de monitoramento"),
    params: Params = Depends(),
    search_monitoring_unit: ISearchMonitoringUnit = Depends(
        Provide[DependencyContainer.search_monitoring_unit]
    ),
):
    query_params: Dict[str, str] = {}
    if name is not None:
        query_params["name"] = name

    input_dto = SearchMonitoringUnitInputDTO(query_params=query_params, pagination=params)
    result = await search_monitoring_unit.execute(input_dto)
    return result


# # 🔎 Buscar por ID
# @router.get("/{id}", responses={404: {"model": ErrorResponseDTO}})
# @inject
# async def get_monitoring_unit_by_id(
#     id: Annotated[int, Path(description="ID da unidade de monitoramento")],
#     get_monitoring_unit_by_id: IGetMonitoringUnitById = Depends(
#         Provide[DependencyContainer.get_monitoring_unit_by_id]
#     ),
# ):
#     result = await get_monitoring_unit_by_id.execute(GetMonitoringUnitByIdInputDTO(id=id))
#     return result


# # ➕ Criar
# @router.post("/", responses={400: {"model": ErrorResponseDTO}})
# @inject
# async def create_monitoring_unit(
#     input: Annotated[CreateMonitoringUnitInputDTO, Body(embed=False)],
#     create_monitoring_unit: ICreateMonitoringUnit = Depends(
#         Provide[DependencyContainer.create_monitoring_unit]
#     ),
# ):
#     result = await create_monitoring_unit.execute(input)
#     return result


# ✏️ Atualizar
# @router.put("/{id}", responses={400: {"model": ErrorResponseDTO}})
# @inject
# async def update_monitoring_unit(
#     id: Annotated[int, Path(description="ID da unidade de monitoramento")],
#     input: Annotated[UpdateMonitoringUnitBodyDTO, Body(embed=False)],
#     update_monitoring_unit: IUpdateMonitoringUnit = Depends(
#         Provide[DependencyContainer.update_monitoring_unit]
#     ),
# ):
#     result = await update_monitoring_unit.execute(
#         UpdateMonitoringUnitInputDTO(id=id, name=input.name)
#     )
#     return result


# ❌ Deletar
# @router.delete("/{id}", responses={400: {"model": ErrorResponseDTO}})
# @inject
# async def delete_monitoring_unit(
#     id: Annotated[int, Path(description="ID da unidade de monitoramento")],
#     delete_monitoring_unit: IDeleteMonitoringUnit = Depends(
#         Provide[DependencyContainer.delete_monitoring_unit]
#     ),
# ):
#     result = await delete_monitoring_unit.execute(DeleteMonitoringUnitInputDTO(id=id))
#     return result


# 🌬️ Listar ar-condicionados associados a uma unidade
@router.get("/{id}/air-conditioners", responses={404: {"model": ErrorResponseDTO}})
@inject
async def get_air_conditioners_by_monitoring_unit(
    id: Annotated[int, Path(description="ID da unidade de monitoramento")],
    find_air_conditioners_by_monitoring_unit: IFindAirConditionersByMonitoringUnit = Depends(
        Provide[DependencyContainer.find_air_conditioners_by_monitoring_unit]
    ),
):
    input_dto = FindAirConditionersByMonitoringUnitInputDTO(monitoring_unit_id=id)
    result = await find_air_conditioners_by_monitoring_unit.execute(input_dto)
    return result
