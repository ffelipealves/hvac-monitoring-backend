from dependency_injector import containers, providers
from monitoring_backend.application.usecases.campus.create_campus import CreateCampus
from monitoring_backend.application.usecases.campus.get_campus_by_id import GetCampusById
from monitoring_backend.application.usecases.campus.search_campus import SearchCampus
from monitoring_backend.application.usecases.campus.update_campus import UpdateCampus
from monitoring_backend.infra.databases.sqlalchemy.connection import Session
from monitoring_backend.infra.databases.sqlalchemy.repositories.campus import (
    CampusDatabaseRepository,
)



class DependencyContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            ".infra.http.routers.campus",
        ]
    )

    session_factory = providers.Object(Session)

    # Repositories
    campus_repository = providers.Singleton(
        CampusDatabaseRepository, session_factory=session_factory
    )

    # Use Cases

    # Users

    # Campuss
    get_campus_by_id = providers.Factory(
        GetCampusById, campus_repository=campus_repository
    )
    create_campus = providers.Factory(CreateCampus, campus_repository=campus_repository)
    update_campus = providers.Factory(UpdateCampus, campus_repository=campus_repository)
    search_campuss = providers.Factory(
        SearchCampus, campus_repository=campus_repository
    )

