from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit


class MonitoringUnitRepository(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[MonitoringUnit]:
        ...

    @abstractmethod
    async def search(
        self,
        query_params: dict,
        offset: int = 0,
        limit: int = 10,
    ) -> Tuple[List[MonitoringUnit], int]:
        ...

    @abstractmethod
    async def create(self, monitoring_unit: MonitoringUnit) -> MonitoringUnit:
        ...

    @abstractmethod
    async def update(self, monitoring_unit: MonitoringUnit) -> MonitoringUnit:
        ...

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[MonitoringUnit]:
        ...

    @abstractmethod
    async def find_by_air_conditioner(self, air_conditioner_id: int) -> Optional[MonitoringUnit]:
        """Retorna a unidade de monitoramento associada a um ar-condicionado específico."""
        ...