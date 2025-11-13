from pydantic import BaseModel, Field
from typing import Optional

from monitoring_backend.domain.vo.name import Name


class AirConditioner(BaseModel):
    """Entidade que representa um ar-condicionado físico."""

    id: Optional[int] = Field(default=None)
    name: Name
    monitoring_unit_id: Optional[int] = Field(default=None)

    model_config = {"frozen": False}  # permite mutações
