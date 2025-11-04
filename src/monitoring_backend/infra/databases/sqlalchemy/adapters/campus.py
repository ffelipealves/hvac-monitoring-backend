from monitoring_backend.domain.vo.name import Name
from monitoring_backend.domain.entity.campus import Campus
from monitoring_backend.infra.databases.sqlalchemy.models.campus import CampusModel


class CampusAdapter:
    @staticmethod
    def entity_to_model(entity: Campus) -> CampusModel:
        return CampusModel(
            id=entity.id,
            name=entity.name.value,
            
        )

    @staticmethod
    def model_to_entity(model: CampusModel) -> Campus:
        return Campus(
            id=model.id,
            name=Name(value=model.name),
        )
