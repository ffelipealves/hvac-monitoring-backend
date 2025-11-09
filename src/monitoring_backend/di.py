from dependency_injector import containers, providers

# Campus
from monitoring_backend.application.usecases.campus.create_campus import CreateCampus
from monitoring_backend.application.usecases.campus.get_campus_by_id import GetCampusById
from monitoring_backend.application.usecases.campus.search_campus import SearchCampus
from monitoring_backend.application.usecases.campus.update_campus import UpdateCampus
from monitoring_backend.infra.databases.sqlalchemy.repositories.campus import (
    CampusDatabaseRepository,
)

# Air Conditioner
from monitoring_backend.application.usecases.air_conditioner.search_air_conditioner import SearchAirConditioner
from monitoring_backend.infra.databases.sqlalchemy.repositories.air_conditioner import (
    AirConditionerDatabaseRepository,
)

from monitoring_backend.application.usecases.monitoring_unit.search_monitoring_unit import SearchMonitoringUnit
from monitoring_backend.application.usecases.monitoring_unit.find_air_conditioners_by_monitoring_unit import FindAirConditionersByMonitoringUnit

from monitoring_backend.infra.databases.sqlalchemy.repositories.monitoring_unit import (
    MonitoringUnitDatabaseRepository,
)

# Sessão do banco
from monitoring_backend.infra.databases.sqlalchemy.connection import Session

class DependencyContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            ".infra.http.routers.campus",
            ".infra.http.routers.air_conditioner",
            ".infra.http.routers.monitoring_unit",# 👈 adiciona o novo router
        ]
    )

    session_factory = providers.Object(Session)

    # ===============================
    # 🧱 Repositories
    # ===============================

    campus_repository = providers.Singleton(
        CampusDatabaseRepository, session_factory=session_factory
    )

    air_conditioner_repository = providers.Singleton(
        AirConditionerDatabaseRepository, session_factory=session_factory
    )
    
    monitoring_unit_repository = providers.Singleton(
        MonitoringUnitDatabaseRepository, session_factory=session_factory
    )

    # ===============================
    # 🧩 Use Cases
    # ===============================

    # Campus
    get_campus_by_id = providers.Factory(
        GetCampusById, campus_repository=campus_repository
    )
    create_campus = providers.Factory(CreateCampus, campus_repository=campus_repository)
    update_campus = providers.Factory(UpdateCampus, campus_repository=campus_repository)
    search_campus = providers.Factory(SearchCampus, campus_repository=campus_repository)

    # Air Conditioners
    search_air_conditioner = providers.Factory(
        SearchAirConditioner, air_conditioner_repository=air_conditioner_repository
    )
    
    # Monitoring Units
    search_monitoring_unit = providers.Factory(
        SearchMonitoringUnit, monitoring_unit_repository=monitoring_unit_repository
    )
    
    find_air_conditioners_by_monitoring_unit = providers.Factory(
        FindAirConditionersByMonitoringUnit, monitoring_unit_repository=monitoring_unit_repository
    )
