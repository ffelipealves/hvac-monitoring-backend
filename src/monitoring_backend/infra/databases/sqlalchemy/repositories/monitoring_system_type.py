from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from typing import List, Optional, Tuple

from monitoring_backend.domain.entity.monitoring_system_type import MonitoringSystemType
from monitoring_backend.application.repositories.monitoring_system_type import MonitoringSystemTypeRepository
from monitoring_backend.infra.databases.sqlalchemy.adapters.monitoring_system_type import MonitoringSystemTypeAdapter
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_system_type import MonitoringSystemTypeModel
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_unit import MonitoringUnitModel


class MonitoringSystemTypeDatabaseRepository(MonitoringSystemTypeRepository):
    """Repositório SQLAlchemy para MonitoringSystemType."""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def get(self, id: int) -> Optional[MonitoringSystemType]:
        async with self._session_factory() as session:
            try:
                stmt = (
                    select(MonitoringSystemTypeModel)
                    .where(MonitoringSystemTypeModel.id == id)
                    .options(selectinload(MonitoringSystemTypeModel.units))
                )
                result = await session.scalar(stmt)

                if result is None:
                    return None

                return MonitoringSystemTypeAdapter.model_to_entity(result)
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar MonitoringSystemType com ID {id}: {e}")

    async def search(
        self, query_params: dict, offset: int = 0, limit: int = 10
    ) -> Tuple[List[MonitoringSystemType], int]:
        async with self._session_factory() as session:
            try:
                stmt = select(MonitoringSystemTypeModel).options(
                    selectinload(MonitoringSystemTypeModel.units)
                )

                # Filtro opcional por nome (ilike)
                if "name" in query_params:
                    stmt = stmt.where(
                        MonitoringSystemTypeModel.name.ilike(f"%{query_params['name']}%")
                    )

                # Contagem total
                total_stmt = select(func.count()).select_from(stmt.subquery())
                total_result = await session.execute(total_stmt)
                total_count = total_result.scalar_one()

                # Paginação
                stmt = stmt.offset(offset).limit(limit)
                result = await session.execute(stmt)
                models = result.scalars().all()

                # Conversão ORM → Entidade
                entities = [
                    MonitoringSystemTypeAdapter.model_to_entity(model) for model in models
                ]
                return entities, total_count

            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar MonitoringSystemTypes: {e}")

    async def create(self, entity: MonitoringSystemType) -> MonitoringSystemType:
        async with self._session_factory() as session:
            try:
                model = MonitoringSystemTypeAdapter.entity_to_model(entity)
                session.add(model)
                await session.commit()
                await session.refresh(model)
                return MonitoringSystemTypeAdapter.model_to_entity(model)
            except SQLAlchemyError as e:
                await session.rollback()
                raise RuntimeError(f"Erro ao criar MonitoringSystemType: {e}")

    async def update(self, entity: MonitoringSystemType) -> MonitoringSystemType:
        async with self._session_factory() as session:
            try:
                stmt = select(MonitoringSystemTypeModel).where(MonitoringSystemTypeModel.id == entity.id)
                result = await session.scalar(stmt)
                if not result:
                    raise RuntimeError(f"MonitoringSystemType com ID {entity.id} não encontrado.")

                # Atualiza campos simples
                result.name = entity.name.value
                result.description = entity.description

                await session.commit()
                await session.refresh(result)
                return MonitoringSystemTypeAdapter.model_to_entity(result)
            except SQLAlchemyError as e:
                await session.rollback()
                raise RuntimeError(f"Erro ao atualizar MonitoringSystemType: {e}")

    async def find_by_name(self, name: str) -> Optional[MonitoringSystemType]:
        async with self._session_factory() as session:
            try:
                stmt = select(MonitoringSystemTypeModel).where(
                    MonitoringSystemTypeModel.name == name
                )
                result = await session.scalar(stmt)
                return (
                    MonitoringSystemTypeAdapter.model_to_entity(result)
                    if result
                    else None
                )
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar MonitoringSystemType pelo nome: {e}")

    async def find_by_unit(self, unit_id: int) -> Optional[MonitoringSystemType]:
        """Retorna o tipo de sistema associado a uma unidade específica."""
        async with self._session_factory() as session:
            try:
                stmt = (
                    select(MonitoringSystemTypeModel)
                    .join(MonitoringSystemTypeModel.units)
                    .where(MonitoringUnitModel.id == unit_id)
                    .options(selectinload(MonitoringSystemTypeModel.units))
                )
                result = await session.scalar(stmt)
                return (
                    MonitoringSystemTypeAdapter.model_to_entity(result)
                    if result
                    else None
                )
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar MonitoringSystemType por unidade: {e}")
