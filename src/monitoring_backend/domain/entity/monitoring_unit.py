from typing import List, Optional
from pydantic import BaseModel, Field

from monitoring_backend.domain.entity.air_conditioner import AirConditioner
from monitoring_backend.domain.vo.name import Name
from monitoring_backend.domain.exceptions.common import InvalidNameException
from monitoring_backend.domain.exceptions.air_conditioner import AirConditionerAlreadyAssociatedException


class MonitoringUnit(BaseModel):
    """Entidade que representa uma unidade de monitoramento (módulo físico)."""

    id: Optional[int] = Field(default=None)
    name: Name
    identifier: str  # ex: número de série, MAC address ou identificador único
    air_conditioners: List[AirConditioner] = Field(default_factory=list)
    monitoring_system_type_id: Optional[int] = Field(default=None)

    model_config = {"frozen": False}  # permite mutações

    def add_air_conditioner(self, air_conditioner: AirConditioner) -> None:
        """Associa um ar-condicionado a esta unidade, garantindo unicidade."""
        # Verifica se já existe um ar-condicionado com o mesmo ID
        if any(ac.id == air_conditioner.id for ac in self.air_conditioners if ac.id is not None):
            raise AirConditionerAlreadyAssociatedException(
                f"Ar-condicionado com id {air_conditioner.id} já está associado a esta unidade."
            )

        # Verifica se já existe um ar-condicionado com o mesmo nome
        for ac in self.air_conditioners:
            if ac.name == air_conditioner.name:
                raise InvalidNameException(
                    f"Ar-condicionado com nome '{air_conditioner.name.value}' já está associado a esta unidade."
                )

        air_conditioner.monitoring_unit_id = self.id  # cria o vínculo reverso
        self.air_conditioners.append(air_conditioner)

    def remove_air_conditioner(self, air_conditioner_id: int) -> None:
        """Remove um ar-condicionado pelo ID."""
        self.air_conditioners = [
            ac for ac in self.air_conditioners if ac.id != air_conditioner_id
        ]

    def get_air_conditioner(self, air_conditioner_id: int) -> Optional[AirConditioner]:
        """Recupera um ar-condicionado específico associado a esta unidade."""
        return next(
            (ac for ac in self.air_conditioners if ac.id == air_conditioner_id),
            None,
        )
