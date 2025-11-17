from typing import List
from datetime import datetime

from dependency_injector.wiring import inject
from pydantic import ValidationError

from monitoring_backend.application.dto.errors import ErrorDetailDTO, ErrorResponseDTO
from monitoring_backend.application.repositories.monitoring_payload import MonitoringPayloadRepository
from monitoring_backend.application.usecases.interfaces.monitoring_payload.create_monitoring_payload import (
    ICreateMonitoringPayload,
    CreateMonitoringPayloadInputDTO,
    CreateMonitoringPayloadOutputDTO,
)
from monitoring_backend.domain.entity.monitoring_payload import MonitoringPayload


class CreateMonitoringPayload(ICreateMonitoringPayload):
    
    @inject
    def __init__(self, monitoring_payload_repository: MonitoringPayloadRepository):
        self.monitoring_payload_repository = monitoring_payload_repository

    async def execute(self, request: CreateMonitoringPayloadInputDTO) -> CreateMonitoringPayloadOutputDTO | ErrorResponseDTO:
        errors: List[ErrorDetailDTO] = []

        # ===========================
        # 🔎 Validação de timestamp
        # ===========================
        timestamp = None
        if request.timestamp is not None:
            try:
                timestamp = datetime.fromisoformat(request.timestamp)
            except ValueError:
                errors.append(
                    ErrorDetailDTO(
                        field="timestamp",
                        message="Timestamp inválido, use formato ISO 8601",
                        code="INVALID_TIMESTAMP",
                    )
                )
        else:
            timestamp = datetime.utcnow()

        # ===========================
        # 🔎 Validação simples dos arrays
        # ===========================
        if request.voltage is not None and not isinstance(request.voltage, list):
            errors.append(ErrorDetailDTO(
                field="voltage",
                message="Voltage deve ser uma lista de floats",
                code="INVALID_VOLTAGE",
            ))

        if request.current is not None and not isinstance(request.current, list):
            errors.append(ErrorDetailDTO(
                field="current",
                message="Current deve ser uma lista de floats",
                code="INVALID_CURRENT",
            ))

        # ===========================
        # 🔎 Verifica erros
        # ===========================
        if errors:
            return ErrorResponseDTO(errors=errors)

        # ===========================
        # 🏗 Criar a entidade de domínio
        # ===========================
        payload = MonitoringPayload(
            id=None,
            monitoring_unit_id=request.monitoring_unit_id,
            air_conditioner_id=request.air_conditioner_id,
            timestamp=timestamp,
            temperature=request.temperature,
            humidity=request.humidity,
            voltage=request.voltage,
            current=request.current,
            extra_data=request.extra_data,
        )

        # ===========================
        # 💾 Persistir no banco
        # ===========================
        saved = await self.monitoring_payload_repository.create(payload)

        # ===========================
        # 📤 Retornar DTO de saída
        # ===========================
        return CreateMonitoringPayloadOutputDTO(
            id=saved.id,
            monitoring_unit_id=saved.monitoring_unit_id,
            air_conditioner_id=saved.air_conditioner_id,
            timestamp=saved.timestamp.isoformat(),
            temperature=saved.temperature,
            humidity=saved.humidity,
            voltage=saved.voltage,
            current=saved.current,
            extra_data=saved.extra_data,
        )
