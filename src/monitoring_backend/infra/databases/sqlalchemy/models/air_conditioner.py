from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class AirConditionerModel(Base):
    __tablename__ = "air_conditioners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Chave estrangeira para MonitoringUnitModel (1-N)
    monitoring_unit_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("monitoring_units.id", ondelete="CASCADE"),
        nullable=True,
    )

    monitoring_unit: Mapped["MonitoringUnitModel"] = relationship(
        back_populates="air_conditioners",
    )
    
    payloads: Mapped[list["MonitoringPayloadModel"]] = relationship(
        back_populates="air_conditioner",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

