from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from monitoring_backend.domain.entity.air_conditioner import AirConditioner


class AirConditionerRepository(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[AirConditioner]:
        ...

    @abstractmethod
    async def search(
        self,
        query_params: dict,
        offset: int = 0,
        limit: int = 10,
    ) -> Tuple[List[AirConditioner], int]:
        ...

    @abstractmethod
    async def create(self, air_conditioner: AirConditioner) -> AirConditioner:
        ...

    @abstractmethod
    async def update(self, air_conditioner: AirConditioner) -> AirConditioner:
        ...

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[AirConditioner]:
        ...

    @abstractmethod
    async def find_by_monitoring_unit(
        self, monitoring_unit_id: int
    ) -> List[AirConditioner]:
        """Retorna todos os ar-condicionados pertencentes a uma unidade de monitoramento."""
        ...
