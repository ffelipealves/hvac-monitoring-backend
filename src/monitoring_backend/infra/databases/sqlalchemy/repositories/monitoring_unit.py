from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from typing import List, Optional, Tuple

from monitoring_backend.domain.entity.monitoring_unit import MonitoringUnit
from monitoring_backend.application.repositories.monitoring_unit import MonitoringUnitRepository
from monitoring_backend.infra.databases.sqlalchemy.adapters.monitoring_unit import MonitoringUnitAdapter
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_unit import MonitoringUnitModel
from monitoring_backend.infra.databases.sqlalchemy.models.air_conditioner import AirConditionerModel



class MonitoringUnitDatabaseRepository(MonitoringUnitRepository):
    """Repositório SQLAlchemy para MonitoringUnit."""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def get(self, id: int) -> Optional[MonitoringUnit]:
        async with self._session_factory() as session:
            try:
                stmt = (
                    select(MonitoringUnitModel)
                    .where(MonitoringUnitModel.id == id)
                    .options(selectinload(MonitoringUnitModel.air_conditioners))  # carrega os ACs juntos
                )
                result = await session.scalar(stmt)

                if result is None:
                    return None

                return MonitoringUnitAdapter.model_to_entity(result)
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar monitoring unit com ID {id}: {e}")

    async def search(
        self, query_params: dict, offset: int = 0, limit: int = 10
    ) -> Tuple[List[MonitoringUnit], int]:
        async with self._session_factory() as session:
            try:
                stmt = select(MonitoringUnitModel).options(
                    selectinload(MonitoringUnitModel.air_conditioners)
                )

                if "name" in query_params:
                    stmt = stmt.where(MonitoringUnitModel.name.ilike(f"%{query_params['name']}%"))

                total_stmt = select(func.count()).select_from(stmt.subquery())
                total_result = await session.execute(total_stmt)
                total_count = total_result.scalar_one()

                stmt = stmt.offset(offset).limit(limit)
                result = await session.execute(stmt)
                models = result.scalars().all()

                entities = [MonitoringUnitAdapter.model_to_entity(model) for model in models]
                return entities, total_count
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar monitoring units: {e}")

    async def create(self, monitoring_unit: MonitoringUnit) -> MonitoringUnit:
        async with self._session_factory() as session:
            try:
                model = MonitoringUnitAdapter.entity_to_model(monitoring_unit)

                session.add(model)
                await session.commit()
                await session.refresh(model, attribute_names=["air_conditioners"])

                return MonitoringUnitAdapter.model_to_entity(model)
            except SQLAlchemyError as e:
                await session.rollback()
                raise RuntimeError(f"Erro ao criar monitoring unit: {e}")

    async def update(self, monitoring_unit: MonitoringUnit) -> MonitoringUnit:
        async with self._session_factory() as session:
            try:
                model = await session.get(
                    MonitoringUnitModel,
                    monitoring_unit.id,
                    options=[selectinload(MonitoringUnitModel.air_conditioners)],
                )

                if not model:
                    raise ValueError(f"MonitoringUnit com id {monitoring_unit.id} não encontrada")

                # Atualiza atributos simples
                model.name = monitoring_unit.name.value
                model.identifier = monitoring_unit.identifier

                # Atualiza os air_conditioners associados
                model.air_conditioners.clear()
                if monitoring_unit.air_conditioners:
                    for ac in monitoring_unit.air_conditioners:
                        ac_model = MonitoringUnitAdapter.entity_to_model(monitoring_unit)
                        model.air_conditioners.append(ac_model)

                await session.commit()
                await session.refresh(model, attribute_names=["air_conditioners"])

                return MonitoringUnitAdapter.model_to_entity(model)
            except SQLAlchemyError as e:
                await session.rollback()
                raise RuntimeError(f"Erro ao atualizar monitoring unit: {e}")

    async def find_by_name(self, name: str) -> Optional[MonitoringUnit]:
        async with self._session_factory() as session:
            stmt = (
                select(MonitoringUnitModel)
                .where(MonitoringUnitModel.name == name)
                .options(selectinload(MonitoringUnitModel.air_conditioners))
            )
            result = await session.execute(stmt)
            model = result.scalars().first()
            return MonitoringUnitAdapter.model_to_entity(model) if model else None
        
    async def find_by_air_conditioner(self, air_conditioner_id: int) -> Optional[MonitoringUnit]:
        async with self._session_factory() as session:
            stmt = (
                select(MonitoringUnitModel)
                .join(AirConditionerModel)
                .where(AirConditionerModel.id == air_conditioner_id)
            )
            result = await session.execute(stmt)
            model = result.scalars().first()
            return MonitoringUnitAdapter.model_to_entity(model) if model else None
