from abc import ABC, abstractmethod
from typing import List, Tuple

from monitoring_backend.domain.entity.campus import Campus


class CampusRepository(ABC):
    @abstractmethod
    async def get(self, id: int) -> Campus: ...

    @abstractmethod
    async def search(
        self, query_params: dict, offset: int = 0, limit: int = 10
    ) -> Tuple[List[Campus], int]:
        ...

    # @abstractmethod
    # def get_all(self):
    #     ...

    @abstractmethod
    async def create(self, campus: Campus): ...

    @abstractmethod
    async def update(self, campus: Campus) -> Campus: ...

    # @abstractmethod
    # def get_all_by_ids(self, ids: List[int]) -> List[Client]:
    #     ...

    @abstractmethod
    async def find_by_name(self, name: str) -> Campus | None: ...

    @abstractmethod
    async def find_by_cnpj(self, cnpj: str) -> Campus | None: ...
