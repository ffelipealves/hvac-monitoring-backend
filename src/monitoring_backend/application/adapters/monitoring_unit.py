from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit

class MonitoringUnitPresenter:
    @staticmethod
    def to_response(monitoring_unit: MonitoringUnit) -> dict:
        return {
            "id": monitoring_unit.id,
            "name": monitoring_unit.name.value,
            "identifier": monitoring_unit.identifier,
            "monitoring_system_type_id": monitoring_unit.monitoring_system_type_id,
            "air_conditioners": [
                {
                    "id": ac.id,
                    "name": ac.name.value
                }
                for ac in monitoring_unit.air_conditioners
            ],
        }
