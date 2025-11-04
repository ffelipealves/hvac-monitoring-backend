from typing import List

from fastapi_pagination import Page
from monitoring_backend.application.adapters.campus import CampusPresenter
from monitoring_backend.application.repositories.campus import CampusRepository
from monitoring_backend.application.usecases.interfaces.campus.search_campus import (
    ISearchCampus,
    SearchCampusInputDTO
)
from monitoring_backend.domain.entity.campus import Campus

from dependency_injector.wiring import inject


class SearchCampus(ISearchCampus):
    @inject
    def __init__(self, campus_repository: CampusRepository):
        self.campus_repository = campus_repository

    async def execute(self, input: SearchCampusInputDTO) -> Page:
        campus, total = await self.campus_repository.search(
            input.query_params,
            offset=(input.pagination.page - 1) * input.pagination.size,
            limit=input.pagination.size,
        )

        if not campus:
            return Page.create(items=[], total=0, params=input.pagination)

        response = []
        for model in campus:
            response.append(CampusPresenter.to_response(model))

        return Page.create(items=response, total=total, params=input.pagination)
