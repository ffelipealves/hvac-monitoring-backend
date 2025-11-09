from monitoring_backend.domain.entity.air_conditioner import AirConditioner

class AirConditionerPresenter:
    @staticmethod
    def to_response(air_conditioner: AirConditioner) -> dict:
        return {
            "id": air_conditioner.id,
            "name": air_conditioner.name.value,
        }
