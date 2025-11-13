from typing import List, Optional
from pydantic import BaseModel, Field

from monitoring_backend.domain.vo.name import Name
from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit
from monitoring_backend.domain.exceptions.common import InvalidNameException


class MonitoringSystemType(BaseModel):
    """Entidade que representa um tipo de sistema de monitoramento."""

    id: Optional[int] = Field(default=None)
    name: Name
    description: Optional[str] = Field(default=None)
    units: List[MonitoringUnit] = Field(default_factory=list)

    model_config = {"frozen": False}  # permite mutações

    def rename(self, new_name: Name) -> None:
        """Atualiza o nome do tipo de sistema."""
        if not new_name or not new_name.value.strip():
            raise InvalidNameException("O nome do tipo de sistema não pode ser vazio.")
        self.name = new_name

    def update_description(self, new_description: Optional[str]) -> None:
        """Atualiza a descrição do tipo de sistema."""
        self.description = new_description

    def add_unit(self, unit: MonitoringUnit) -> None:
        """Associa uma unidade de monitoramento a este tipo de sistema."""
        # Verifica se já existe uma unidade com o mesmo ID
        if any(u.id == unit.id for u in self.units if u.id is not None):
            return  # evita duplicação

        # Cria vínculo reverso se aplicável
        unit.monitoring_system_type_id = self.id
        self.units.append(unit)

    def remove_unit(self, unit_id: int) -> None:
        """Remove uma unidade associada a este tipo de sistema."""
        self.units = [u for u in self.units if u.id != unit_id]

    def get_unit(self, unit_id: int) -> Optional[MonitoringUnit]:
        """Recupera uma unidade específica associada a este tipo de sistema."""
        return next((u for u in self.units if u.id == unit_id), None)
