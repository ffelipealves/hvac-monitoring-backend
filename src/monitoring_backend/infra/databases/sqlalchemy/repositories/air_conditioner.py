from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Tuple

from monitoring_backend.domain.entity.air_conditioner import AirConditioner
from monitoring_backend.application.repositories.air_conditioner import AirConditionerRepository
from monitoring_backend.infra.databases.sqlalchemy.adapters.air_conditioner import AirConditionerAdapter
from monitoring_backend.infra.databases.sqlalchemy.models.air_conditioner import AirConditionerModel


class AirConditionerDatabaseRepository(AirConditionerRepository):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def get(self, id: int) -> Optional[AirConditioner]:
        async with self._session_factory() as session:
            try:
                stmt = select(AirConditionerModel).where(AirConditionerModel.id == id)
                result = await session.scalar(stmt)

                if result is None:
                    return None

                return AirConditionerAdapter.model_to_entity(result)
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar ar-condicionado com ID {id}: {e}")

    async def search(
        self,
        query_params: dict,
        offset: int = 0,
        limit: int = 10,
    ) -> Tuple[List[AirConditioner], int]:
        async with self._session_factory() as session:
            try:
                stmt = select(AirConditionerModel)

                # Filtro por nome
                if "name" in query_params:
                    stmt = stmt.where(AirConditionerModel.name.ilike(f"%{query_params['name']}%"))

                # Filtro por unidade de monitoramento
                if "monitoring_unit_id" in query_params:
                    stmt = stmt.where(
                        AirConditionerModel.monitoring_unit_id == int(query_params["monitoring_unit_id"])
                    )

                total_stmt = select(func.count()).select_from(stmt.subquery())
                total_result = await session.execute(total_stmt)
                total_count = total_result.scalar_one()

                stmt = stmt.offset(offset).limit(limit)
                result = await session.execute(stmt)
                models = result.scalars().all()

                entities = [AirConditionerAdapter.model_to_entity(model) for model in models]

                return entities, total_count
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar ar-condicionado: {e}")

    async def create(self, air_conditioner: AirConditioner) -> AirConditioner:
        async with self._session_factory() as session:
            model = AirConditionerAdapter.entity_to_model(air_conditioner)

            session.add(model)
            await session.commit()
            await session.refresh(model)

            return AirConditionerAdapter.model_to_entity(model)

    async def update(self, air_conditioner: AirConditioner) -> AirConditioner:
        async with self._session_factory() as session:
            model = await session.get(AirConditionerModel, air_conditioner.id)

            if not model:
                raise ValueError(f"Ar-condicionado com id {air_conditioner.id} não encontrado")

            model.name = air_conditioner.name.value
            model.monitoring_unit_id = air_conditioner.monitoring_unit_id  # ✅ atualização da FK

            await session.commit()
            await session.refresh(model)
            return AirConditionerAdapter.model_to_entity(model)

    async def find_by_name(self, name: str) -> Optional[AirConditioner]:
        async with self._session_factory() as session:
            stmt = select(AirConditionerModel).where(AirConditionerModel.name == name)
            result = await session.execute(stmt)
            model = result.scalars().first()
            return AirConditionerAdapter.model_to_entity(model) if model else None

    async def find_by_monitoring_unit(
        self, monitoring_unit_id: int
    ) -> List[AirConditioner]:
        """Retorna todos os ACs de uma unidade de monitoramento específica."""
        async with self._session_factory() as session:
            stmt = select(AirConditionerModel).where(
                AirConditionerModel.monitoring_unit_id == monitoring_unit_id
            )
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [AirConditionerAdapter.model_to_entity(model) for model in models]
