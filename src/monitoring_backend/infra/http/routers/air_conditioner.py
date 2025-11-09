from typing import Annotated, Dict, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi_pagination import Page, Params

from monitoring_backend.application.dto.errors import ErrorResponseDTO
# from monitoring_backend.application.usecases.interfaces.air_conditioner.create_air_conditioner import (
#     ICreateAirConditioner,
#     CreateAirConditionerInputDTO,
# )
# from monitoring_backend.application.usecases.interfaces.air_conditioner.get_air_conditioner_by_id import (
#     IGetAirConditionerById,
#     GetAirConditionerByIdInputDTO,
# )
from monitoring_backend.application.usecases.interfaces.air_conditioner.search_air_conditioner import (
    ISearchAirConditioner,
    SearchAirConditionerInputDTO,
)
# from monitoring_backend.application.usecases.interfaces.air_conditioner.update_air_conditioner import (
#     IUpdateAirConditioner,
#     UpdateAirConditionerBodyDTO,
#     UpdateAirConditionerInputDTO,
# )
from monitoring_backend.di import DependencyContainer


router = APIRouter(
    prefix="/air-conditioner",
    tags=["air-conditioner"],
)


# 🔍 Buscar (com paginação)
# NAO ESTA FUNCIONADNO PARAMETROS
@router.get("/search", response_model=Page, responses={400: {"model": ErrorResponseDTO}})
@inject
async def search_air_conditioners(
    name: Optional[str] = Query(None, description="Filtrar por nome do ar-condicionado"),
    monitoring_unit_id: Optional[int] = Query(None, description="Filtrar por ID da unidade de monitoramento"),
    params: Params = Depends(),
    search_air_conditioner: ISearchAirConditioner = Depends(
        Provide[DependencyContainer.search_air_conditioner]
    ),
):
    query_params: Dict[str, str] = {}
    if name is not None:
        query_params["name"] = name
    if monitoring_unit_id is not None:
        query_params["monitoring_unit_id"] = str(monitoring_unit_id)

    input_dto = SearchAirConditionerInputDTO(query_params=query_params, pagination=params)
    result = await search_air_conditioner.execute(input_dto)
    return result



# # 🔎 Buscar por ID
# @router.get("/{id}", responses={404: {"model": ErrorResponseDTO}})
# @inject
# async def get_air_conditioner_by_id(
#     id: Annotated[int, Path(description="ID do ar-condicionado")],
#     get_air_conditioner_by_id: IGetAirConditionerById = Depends(Provide[DependencyContainer.get_air_conditioner_by_id]),
# ):
#     result = await get_air_conditioner_by_id.execute(GetAirConditionerByIdInputDTO(id=id))
#     return result


# # ➕ Criar
# @router.post("/", responses={400: {"model": ErrorResponseDTO}})
# @inject
# async def create_air_conditioner(
#     input: Annotated[CreateAirConditionerInputDTO, Body(embed=False)],
#     monitoring_unit_id: Optional[int] = Query(
#         None, description="ID da unidade de monitoramento associada (opcional)"
#     ),
#     create_air_conditioner: ICreateAirConditioner = Depends(
#         Provide[DependencyContainer.create_air_conditioner]
#     ),
# ):
#     if monitoring_unit_id is not None:
#         input.monitoring_unit_id = monitoring_unit_id
#     result = await create_air_conditioner.execute(input)
#     return result



# ✏️ Atualizar
# @router.put("/{id}", responses={400: {"model": ErrorResponseDTO}})
# @inject
# async def update_air_conditioner(
#     id: Annotated[int, Path(description="ID do ar-condicionado")],
#     input: Annotated[UpdateAirConditionerBodyDTO, Body(embed=False)],
#     update_air_conditioner: IUpdateAirConditioner = Depends(Provide[DependencyContainer.update_air_conditioner]),
# ):
#     result = await update_air_conditioner.execute(UpdateAirConditionerInputDTO(id=id, name=input.name))
#     return result
