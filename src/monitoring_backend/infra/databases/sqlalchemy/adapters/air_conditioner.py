from monitoring_backend.domain.vo.name import Name
from monitoring_backend.domain.entity.air_conditioner import AirConditioner
from monitoring_backend.infra.databases.sqlalchemy.models.air_conditioner import AirConditionerModel


class AirConditionerAdapter:
    """Converte entre entidade AirConditioner e modelo SQLAlchemy."""

    @staticmethod
    def entity_to_model(entity: AirConditioner) -> AirConditionerModel:
        return AirConditionerModel(
            id=entity.id,
            name=entity.name.value,
            # monitoring_unit_id pode ser None ou já vir setado na entidade
            monitoring_unit_id=getattr(entity, "monitoring_unit_id", None),
        )

    @staticmethod
    def model_to_entity(model: AirConditionerModel) -> AirConditioner:
        return AirConditioner(
            id=model.id,
            name=Name(value=model.name),
            monitoring_unit_id=model.monitoring_unit_id,
        )
