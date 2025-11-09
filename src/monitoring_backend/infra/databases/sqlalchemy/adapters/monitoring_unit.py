from monitoring_backend.domain.vo.name import Name
from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_unit import MonitoringUnitModel
from monitoring_backend.infra.databases.sqlalchemy.adapters.air_conditioner import AirConditionerAdapter


class MonitoringUnitAdapter:
    """Converte entre entidade MonitoringUnit e modelo SQLAlchemy."""

    @staticmethod
    def entity_to_model(entity: MonitoringUnit) -> MonitoringUnitModel:
        model = MonitoringUnitModel(
            id=entity.id,
            name=entity.name.value,
            identifier=entity.identifier,
        )

        # Converter os AirConditioners associados (1-N)
        if getattr(entity, "air_conditioners", None):
            model.air_conditioners = [
                AirConditionerAdapter.entity_to_model(ac) for ac in entity.air_conditioners
            ]

        return model

    @staticmethod
    def model_to_entity(model: MonitoringUnitModel) -> MonitoringUnit:
        return MonitoringUnit(
            id=model.id,
            name=Name(value=model.name),
            identifier=model.identifier,
            air_conditioners=[
                AirConditionerAdapter.model_to_entity(ac) for ac in model.air_conditioners
            ] if model.air_conditioners else [],
        )
