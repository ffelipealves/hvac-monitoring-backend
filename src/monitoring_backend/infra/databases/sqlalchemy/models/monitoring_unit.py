from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class MonitoringUnitModel(Base):
    __tablename__ = "monitoring_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    identifier: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Relacionamento 1-N com AirConditionerModel
    air_conditioners: Mapped[list["AirConditionerModel"]] = relationship(
        back_populates="monitoring_unit",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
