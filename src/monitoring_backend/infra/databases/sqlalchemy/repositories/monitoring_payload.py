from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Tuple

from monitoring_backend.domain.entity.monitoring_payload import MonitoringPayload
from monitoring_backend.application.repositories.monitoring_payload import MonitoringPayloadRepository
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_payload import MonitoringPayloadModel
from monitoring_backend.infra.databases.sqlalchemy.adapters.monitoring_payload import MonitoringPayloadAdapter


class MonitoringPayloadDatabaseRepository(MonitoringPayloadRepository):
    """Implementação concreta do repositório de MonitoringPayload usando SQLAlchemy."""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def get(self, id: int) -> Optional[MonitoringPayload]:
        async with self._session_factory() as session:
            try:
                stmt = select(MonitoringPayloadModel).where(MonitoringPayloadModel.id == id)
                result = await session.scalar(stmt)
                return MonitoringPayloadAdapter.model_to_entity(result) if result else None
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar payload com ID {id}: {e}")

    async def search(
        self,
        query_params: dict,
        offset: int = 0,
        limit: int = 10,
    ) -> Tuple[List[MonitoringPayload], int]:
        async with self._session_factory() as session:
            try:
                stmt = select(MonitoringPayloadModel)

                # 🔍 Filtros dinâmicos
                if "monitoring_unit_id" in query_params:
                    stmt = stmt.where(MonitoringPayloadModel.monitoring_unit_id == int(query_params["monitoring_unit_id"]))
                if "air_conditioner_id" in query_params:
                    stmt = stmt.where(MonitoringPayloadModel.air_conditioner_id == int(query_params["air_conditioner_id"]))

                total_stmt = select(func.count()).select_from(stmt.subquery())
                total_result = await session.execute(total_stmt)
                total_count = total_result.scalar_one()

                stmt = stmt.offset(offset).limit(limit)
                result = await session.execute(stmt)
                models = result.scalars().all()

                entities = [MonitoringPayloadAdapter.model_to_entity(model) for model in models]

                return entities, total_count
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar payloads: {e}")

    async def create(self, payload: MonitoringPayload) -> MonitoringPayload:
        async with self._session_factory() as session:
            try:
                model = MonitoringPayloadAdapter.entity_to_model(payload)
                session.add(model)
                await session.commit()
                await session.refresh(model)
                return MonitoringPayloadAdapter.model_to_entity(model)
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao criar payload: {e}")

    async def update(self, payload: MonitoringPayload) -> MonitoringPayload:
        async with self._session_factory() as session:
            try:
                model = await session.get(MonitoringPayloadModel, payload.id)
                if not model:
                    raise ValueError(f"Payload com id {payload.id} não encontrado")

                # Atualiza campos principais
                model.temperature = payload.temperature
                model.humidity = payload.humidity
                model.energy_consumption = payload.energy_consumption

                await session.commit()
                await session.refresh(model)
                return MonitoringPayloadAdapter.model_to_entity(model)
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao atualizar payload: {e}")

    async def delete(self, id: int) -> None:
        async with self._session_factory() as session:
            try:
                model = await session.get(MonitoringPayloadModel, id)
                if not model:
                    raise ValueError(f"Payload com id {id} não encontrado")
                await session.delete(model)
                await session.commit()
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao deletar payload: {e}")

    async def find_by_monitoring_unit(self, monitoring_unit_id: int) -> List[MonitoringPayload]:
        async with self._session_factory() as session:
            stmt = select(MonitoringPayloadModel).where(
                MonitoringPayloadModel.monitoring_unit_id == monitoring_unit_id
            )
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [MonitoringPayloadAdapter.model_to_entity(m) for m in models]

    async def find_by_air_conditioner(self, air_conditioner_id: int) -> List[MonitoringPayload]:
        async with self._session_factory() as session:
            stmt = select(MonitoringPayloadModel).where(
                MonitoringPayloadModel.air_conditioner_id == air_conditioner_id
            )
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [MonitoringPayloadAdapter.model_to_entity(m) for m in models]
