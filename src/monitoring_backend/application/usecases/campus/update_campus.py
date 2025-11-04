from typing import List, Union

from pydantic import ValidationError
from dependency_injector.wiring import inject

from monitoring_backend.application.dto.errors import ErrorDetailDTO, ErrorResponseDTO
from monitoring_backend.application.repositories.campus import CampusRepository
from monitoring_backend.application.usecases.interfaces.campus.update_campus import (
    IUpdateCampus,
    UpdateCampusInputDTO,
    UpdateCampusOutputDTO,
)
from monitoring_backend.domain.entity.campus import Campus
from monitoring_backend.domain.vo.name import Name, InvalidNameException


class UpdateCampus(IUpdateCampus):
    """Caso de uso para atualização de campus."""

    @inject
    def __init__(self, campus_repository: CampusRepository):
        self.campus_repository = campus_repository

    async def execute(
        self, input: UpdateCampusInputDTO
    ) -> Union[UpdateCampusOutputDTO, ErrorResponseDTO]:
        """
        Atualiza os dados de um campus.
        Retorna DTO de sucesso ou erro.
        """
        errors: List[ErrorDetailDTO] = []

        campus_model = await self.campus_repository.get(input.id)

        if campus_model is None:
            return ErrorResponseDTO(
                errors=[
                    ErrorDetailDTO(
                        field=None, message="Campus não encontrado", code="NOT_FOUND"
                    )
                ]
            )

        name_vo = None

        # Validação dos VOs
        if input.name:
            try:
                name_vo = Name(value=input.name)
            except (ValidationError, InvalidNameException) as e:
                errors.append(
                    ErrorDetailDTO(field="name", message=str(e), code="INVALID_NAME")
                )

        # Validação de unicidade (apenas se VOs válidos)
        if not errors:
            if input.name and input.name != str(campus_model.name):
                existing_campus = await self.campus_repository.find_by_name(input.name)
                if existing_campus and existing_campus.id != input.id:
                    errors.append(
                        ErrorDetailDTO(
                            field="name",
                            message="Já existe campus com este nome",
                            code="DUPLICATE_NAME",
                        )
                    )


        # Retorna DTO de erro se houver algum problema
        if errors:
            return ErrorResponseDTO(errors=errors)

        # Criação e persistência do campus
        campus = Campus(
            id=input.id,
            name=name_vo or campus_model.name,
        )
        updated = await self.campus_repository.update(campus)

        return UpdateCampusOutputDTO(
            id=updated.id, name=str(updated.name)
        )
