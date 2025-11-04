from monitoring_backend.domain.entity.campus import Campus

class CampusPresenter:
    @staticmethod
    def to_response(campus: Campus) -> dict:
        return {
            "id": campus.id,
            "name": campus.name.value,
        }
