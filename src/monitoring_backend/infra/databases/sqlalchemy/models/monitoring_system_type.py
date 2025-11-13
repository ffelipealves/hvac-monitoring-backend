from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class MonitoringSystemTypeModel(Base):
    __tablename__ = "monitoring_system_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # 1-N com MonitoringUnitModel
    units: Mapped[list["MonitoringUnitModel"]] = relationship(
        back_populates="system_type",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
