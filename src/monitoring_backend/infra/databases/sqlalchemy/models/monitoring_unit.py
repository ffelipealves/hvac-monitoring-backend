from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class MonitoringUnitModel(Base):
    __tablename__ = "monitoring_units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    identifier: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # 1-N com AirConditionerModel
    air_conditioners: Mapped[list["AirConditionerModel"]] = relationship(
        back_populates="monitoring_unit",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # 1-N com MonitoringPayloadModel ✅
    payloads: Mapped[list["MonitoringPayloadModel"]] = relationship(
        back_populates="monitoring_unit",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    
    # chave estrangeira para MonitoringSystemType
    monitoring_system_type_id: Mapped[int | None] = mapped_column(
        ForeignKey("monitoring_system_types.id", ondelete="SET NULL"),
        nullable=True,
    )

    system_type = relationship(
        "MonitoringSystemTypeModel",
        back_populates="units",
    )
