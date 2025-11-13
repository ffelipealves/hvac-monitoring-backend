from monitoring_backend.domain.entity.monitoring_payload import MonitoringPayload
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_payload import MonitoringPayloadModel


class MonitoringPayloadAdapter:
    """Responsável por converter entre Model <-> Entity de MonitoringPayload."""

    @staticmethod
    def model_to_entity(model: MonitoringPayloadModel) -> MonitoringPayload:
        if not model:
            return None

        return MonitoringPayload(
            id=model.id,
            monitoring_unit_id=model.monitoring_unit_id,
            air_conditioner_id=model.air_conditioner_id,
            timestamp=model.timestamp,
            temperature=model.temperature,
            humidity=model.humidity,
            power_consumption=model.power_consumption,
            extra_data=model.extra_data or {},
        )

    @staticmethod
    def entity_to_model(entity: MonitoringPayload) -> MonitoringPayloadModel:
        return MonitoringPayloadModel(
            id=entity.id,
            monitoring_unit_id=entity.monitoring_unit_id,
            air_conditioner_id=entity.air_conditioner_id,
            timestamp=entity.timestamp,
            temperature=entity.temperature,
            humidity=entity.humidity,
            power_consumption=entity.power_consumption,
            extra_data=entity.extra_data,
        )
