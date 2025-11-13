from monitoring_backend.domain.vo.name import Name
from monitoring_backend.domain.entity.monitoring_system_type import MonitoringSystemType
from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_system_type import MonitoringSystemTypeModel
from monitoring_backend.infra.databases.sqlalchemy.adapters.monitoring_unit import MonitoringUnitAdapter


class MonitoringSystemTypeAdapter:
    """Converte entre a entidade MonitoringSystemType e o modelo SQLAlchemy."""

    @staticmethod
    def entity_to_model(entity: MonitoringSystemType) -> MonitoringSystemTypeModel:
        """Converte uma entidade de domínio para o modelo ORM."""
        model = MonitoringSystemTypeModel(
            id=entity.id,
            name=entity.name.value,
            description=entity.description,
        )

        # Converter as MonitoringUnits associadas (1-N)
        if getattr(entity, "units", None):
            model.units = [
                MonitoringUnitAdapter.entity_to_model(unit) for unit in entity.units
            ]

        return model

    @staticmethod
    def model_to_entity(model: MonitoringSystemTypeModel) -> MonitoringSystemType:
        """Converte um modelo ORM para a entidade de domínio."""
        return MonitoringSystemType(
            id=model.id,
            name=Name(value=model.name),
            description=model.description,
            units=[
                MonitoringUnitAdapter.model_to_entity(unit) for unit in model.units
            ] if model.units else [],
        )
