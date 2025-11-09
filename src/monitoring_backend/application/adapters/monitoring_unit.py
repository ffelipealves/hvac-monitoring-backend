from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit

class MonitoringUnitPresenter:
    @staticmethod
    def to_response(monitoring_unit: MonitoringUnit) -> dict:
        return {
            "id": monitoring_unit.id,
            "name": monitoring_unit.name.value,
            "identifier": monitoring_unit.identifier,
            "air_conditioners": [
                {
                    "id": ac.id,
                    "name": ac.name.value
                }
                for ac in monitoring_unit.air_conditioners
            ],
        }
