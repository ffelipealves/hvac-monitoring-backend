from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

from monitoring_backend.domain.entity.monitoring_payload import MonitoringPayload


class MonitoringPayloadRepository(ABC):
    """Contrato base para repositórios de MonitoringPayload."""

    @abstractmethod
    async def get(self, id: int) -> Optional[MonitoringPayload]:
        """Obtém um payload específico pelo ID."""
        ...

    @abstractmethod
    async def search(
        self,
        query_params: dict,
        offset: int = 0,
        limit: int = 10,
    ) -> Tuple[List[MonitoringPayload], int]:
        """Busca payloads com base em filtros e paginação."""
        ...

    @abstractmethod
    async def create(self, payload: MonitoringPayload) -> MonitoringPayload:
        """Cria um novo registro de payload."""
        ...

    @abstractmethod
    async def update(self, payload: MonitoringPayload) -> MonitoringPayload:
        """Atualiza um registro de payload existente."""
        ...

    @abstractmethod
    async def delete(self, id: int) -> None:
        """Deleta um registro de payload."""
        ...

    @abstractmethod
    async def find_by_monitoring_unit(
        self, monitoring_unit_id: int
    ) -> List[MonitoringPayload]:
        """Retorna todos os payloads associados a uma unidade de monitoramento."""
        ...

    @abstractmethod
    async def find_by_air_conditioner(
        self, air_conditioner_id: int
    ) -> List[MonitoringPayload]:
        """Retorna todos os payloads associados a um ar-condicionado."""
        ...
