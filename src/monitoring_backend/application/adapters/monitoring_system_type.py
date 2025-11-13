from monitoring_backend.domain.entity.monitoring_system_type import MonitoringSystemType


class MonitoringSystemTypePresenter:
    """Responsável por transformar a entidade MonitoringSystemType em um formato de resposta (dict)."""

    @staticmethod
    def to_response(monitoring_system_type: MonitoringSystemType) -> dict:
        """Converte um tipo de sistema de monitoramento em um dicionário serializável."""
        return {
            "id": monitoring_system_type.id,
            "name": monitoring_system_type.name.value,
            "description": monitoring_system_type.description,
            "units": [
                {
                    "id": unit.id,
                    "name": unit.name.value,
                    "identifier": unit.identifier,
                    "monitoring_system_type_id": unit.monitoring_system_type_id,
                }
                for unit in monitoring_system_type.units
            ],
        }