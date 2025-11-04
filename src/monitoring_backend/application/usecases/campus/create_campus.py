from typing import List

from pydantic import ValidationError
from monitoring_backend.application.dto.errors import ErrorDetailDTO, ErrorResponseDTO
from monitoring_backend.application.repositories.campus import CampusRepository
from monitoring_backend.application.usecases.interfaces.campus.create_campus import CreateCampusInputDTO, CreateCampusOutputDTO, ICreateCampus
from monitoring_backend.domain.entity.campus import Campus
from monitoring_backend.domain.exceptions.common import InvalidNameException
from monitoring_backend.domain.vo.name import Name

from dependency_injector.wiring import inject

class CreateCampus(ICreateCampus):
    @inject
    def __init__(self, campus_repository: CampusRepository):
        self.campus_repository = campus_repository

    async def execute(self, request: CreateCampusInputDTO) -> CreateCampusOutputDTO | ErrorResponseDTO:
        errors: List[ErrorDetailDTO] = []

        # Validação dos VOs
        try:
            name_vo = Name(value=request.name)
        except ValidationError as e:
            errors.append(ErrorDetailDTO(field="name", message=str(e), code="INVALID_NAME"))
        except InvalidNameException as e:
            errors.append(ErrorDetailDTO(field="name", message=str(e), code="INVALID_NAME"))

        # Validação de unicidade (apenas se VOs válidos)
        if not errors:
            if await self.campus_repository.find_by_name(request.name):
                errors.append(ErrorDetailDTO(field="name", message="Já existe um campus com esse nome", code="DUPLICATE_NAME"))

        # Retorna DTO de erro se houver algum problema
        if errors:
            return ErrorResponseDTO(errors=errors)

        # Criação e persistência do campus
        campus = Campus(name=name_vo)
        saved = await self.campus_repository.create(campus)

        return CreateCampusOutputDTO(id=saved.id, name=str(saved.name))
