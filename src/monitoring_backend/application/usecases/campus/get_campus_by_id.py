from typing import List
from monitoring_backend.application.dto.errors import ErrorDetailDTO, ErrorResponseDTO
from monitoring_backend.application.repositories.campus import CampusRepository
from monitoring_backend.application.usecases.interfaces.campus.get_campus_by_id import GetCampusByIdInputDTO, GetCampusByIdOutputDTO, IGetCampusById
from monitoring_backend.domain.entity.campus import Campus
from monitoring_backend.domain.vo.name import InvalidNameException, Name


from dependency_injector.wiring import inject

class GetCampusById(IGetCampusById):
    @inject
    def __init__(self, campus_repository: CampusRepository):
        self.campus_repository = campus_repository

    async def execute(self, input: GetCampusByIdInputDTO) -> GetCampusByIdOutputDTO | ErrorResponseDTO:
        campus: Campus | None = await self.campus_repository.get(input.id)

        if campus is None:
            return ErrorResponseDTO(
                errors=[
                    ErrorDetailDTO(
                        field="id",
                        message=f"Campuse com id {input.id} não encontrado",
                        code="CLIENT_NOT_FOUND",
                    )
                ]
            )

        return GetCampusByIdOutputDTO(
            id=campus.id,
            name=str(campus.name),
        )
