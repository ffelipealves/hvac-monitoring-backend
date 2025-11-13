from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from monitoring_backend.domain.entity.monitoring_system_type import MonitoringSystemType


class MonitoringSystemTypeRepository(ABC):
    """Interface de repositório para a entidade MonitoringSystemType."""

    @abstractmethod
    async def get(self, id: int) -> Optional[MonitoringSystemType]:
        """Recupera um tipo de sistema de monitoramento pelo ID."""
        ...

    @abstractmethod
    async def search(
        self,
        query_params: dict,
        offset: int = 0,
        limit: int = 10,
    ) -> Tuple[List[MonitoringSystemType], int]:
        """Busca tipos de sistema com filtros e paginação."""
        ...

    @abstractmethod
    async def create(self, monitoring_system_type: MonitoringSystemType) -> MonitoringSystemType:
        """Cria um novo tipo de sistema de monitoramento."""
        ...

    @abstractmethod
    async def update(self, monitoring_system_type: MonitoringSystemType) -> MonitoringSystemType:
        """Atualiza um tipo de sistema de monitoramento existente."""
        ...

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[MonitoringSystemType]:
        """Busca um tipo de sistema de monitoramento pelo nome."""
        ...

    @abstractmethod
    async def find_by_unit(self, unit_id: int) -> Optional[MonitoringSystemType]:
        """Retorna o tipo de sistema associado a uma unidade específica."""
        ...
