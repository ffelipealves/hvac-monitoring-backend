from typing import Annotated, Dict, Optional
from datetime import datetime
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi_pagination import Page, Params
from monitoring_backend.application.dto.errors import ErrorResponseDTO
from monitoring_backend.application.usecases.interfaces.campus.create_campus import CreateCampusInputDTO, ICreateCampus
from monitoring_backend.application.usecases.interfaces.campus.get_campus_by_id import GetCampusByIdInputDTO, IGetCampusById
from monitoring_backend.application.usecases.interfaces.campus.search_campus import ISearchCampus, SearchCampusInputDTO
from monitoring_backend.application.usecases.interfaces.campus.update_campus import IUpdateCampus, UpdateCampusBodyDTO, UpdateCampusInputDTO
from monitoring_backend.di import DependencyContainer
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, Depends, Path, Query


router = APIRouter(
    prefix="/campuss",
    tags=["campuss"],
)

@router.get("/search", response_model=Page)
@inject
async def search(
    name: Optional[str] = Query(None, description="Filter by campus name"),
    cnpj: Optional[str] = Query(None, description="Filter by campus CNPJ"),
    params: Params = Depends(),
    search_campuss: ISearchCampus = Depends(Provide[DependencyContainer.search_campuss]),
):
    query_params: Dict[str, str] = {}

    if name is not None:
        query_params["name"] = name
    if cnpj is not None:
        query_params["cnpj"] = cnpj

    search_campuss_input = SearchCampusInputDTO(query_params=query_params, pagination=params)
    result = await search_campuss.execute(search_campuss_input)
    return result

@router.get("/{id}")
@inject
async def get_campus_by_id(
    id: Annotated[int, Path(description="ID do campuse")],
    get_campus_by_id: IGetCampusById = Depends(Provide[DependencyContainer.get_campus_by_id]),
):
    result = await get_campus_by_id.execute(GetCampusByIdInputDTO(id=id))
    return result

@router.post("/")
@inject
async def create(
    input: Annotated[CreateCampusInputDTO, Body(embed=False)],
    create_campus: ICreateCampus = Depends(Provide[DependencyContainer.create_campus]),
):
    result = await create_campus.execute(input)
    return result

@router.put("/{id}")
@inject
async def update(
    id: Annotated[int, Path(description="ID do campuse")],
    input: Annotated[UpdateCampusBodyDTO, Body(embed=False)],
    update_campus: IUpdateCampus = Depends(Provide[DependencyContainer.update_campus]),
):
    result = await update_campus.execute(UpdateCampusInputDTO(id=id, name=input.name, cnpj=input.cnpj))
    return result

