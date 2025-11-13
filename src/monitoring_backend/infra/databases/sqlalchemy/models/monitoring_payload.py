from datetime import datetime
from sqlalchemy import Integer, ForeignKey, Float, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class MonitoringPayloadModel(Base):
    __tablename__ = "monitoring_payloads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    monitoring_unit_id: Mapped[int] = mapped_column(
        ForeignKey("monitoring_units.id", ondelete="CASCADE"), nullable=False
    )
    air_conditioner_id: Mapped[int] = mapped_column(
        ForeignKey("air_conditioners.id", ondelete="CASCADE"), nullable=False
    )

    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity: Mapped[float | None] = mapped_column(Float, nullable=True)
    power_consumption: Mapped[float | None] = mapped_column(Float, nullable=True)
    extra_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    monitoring_unit = relationship("MonitoringUnitModel", back_populates="payloads")
    air_conditioner = relationship("AirConditionerModel", back_populates="payloads")
