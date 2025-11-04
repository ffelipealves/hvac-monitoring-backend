from sqlalchemy import func, select
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple

from monitoring_backend.domain.entity.campus import Campus
from monitoring_backend.domain.vo.name import Name
from monitoring_backend.application.repositories.campus import CampusRepository
from monitoring_backend.infra.databases.sqlalchemy.adapters.campus import CampusAdapter
from monitoring_backend.infra.databases.sqlalchemy.models.campus import CampusModel

from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError


class CampusDatabaseRepository(CampusRepository):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def get(self, id: str) -> Optional[Campus]:
        async with self._session_factory() as session:
            try:
                stmt = (
                    select(CampusModel)
                    .where(CampusModel.id == id)
                )

                result = await session.scalar(stmt)

                if result is None:
                    return None

                return CampusAdapter.model_to_entity(result)
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar campus com ID {id}: {e}")
            
    async def search(
        self, query_params: dict, offset: int = 0, limit: int = 10
    ) -> Tuple[List[Campus], int]:
        async with self._session_factory() as session:
            try:
                stmt = select(CampusModel)
                if "name" in query_params:
                    stmt = stmt.where(CampusModel.name.ilike(f"%{query_params['name']}%"))
                if "cnpj" in query_params:
                    stmt = stmt.where(CampusModel.cnpj == query_params["cnpj"])

                total_stmt = select(func.count()).select_from(stmt.subquery())
                total_result = await session.execute(total_stmt)
                total_count = total_result.scalar_one()

                stmt = stmt.offset(offset).limit(limit)

                result = await session.execute(stmt)
                models = result.scalars().all()

                entities = [CampusAdapter.model_to_entity(model) for model in models]

                return entities, total_count
            except SQLAlchemyError as e:
                raise RuntimeError(f"Erro ao buscar campus: {e}")

    # def get_all(self) -> List[Client]:
    #     models = self.session.query(ClientModel).all()
    #     return [self._model_to_entity(m) for m in models]

    async def create(self, campus: Campus) -> Campus:
        async with self._session_factory() as session:
            model = CampusAdapter.entity_to_model(campus)

            session.add(model)
            await session.commit()
            await session.refresh(model)

            return CampusAdapter.model_to_entity(model)


    async def update(self, campus: Campus) -> Campus:
        async with self._session_factory() as session:
            model = await session.get(CampusModel, campus.id)

            if not model:
                raise ValueError(f"Campus with id {campus.id} not found")

            model.name = str(campus.name)

            await session.commit()
            await session.refresh(model)
            return CampusAdapter.model_to_entity(model)

    # def get_all_by_ids(self, ids: List[str]) -> List[Client]:
    #     models = self.session.query(ClientModel).filter(ClientModel.id.in_(ids)).all()
    #     return [self._model_to_entity(m) for m in models]

    async def find_by_name(self, name: str) -> Optional[Campus]:
        async with self._session_factory() as session:

            stmt = (
                select(CampusModel)
                .where(CampusModel.name == name)
            )

            result = await session.execute(stmt)
            model = result.scalars().first()
            return CampusAdapter.model_to_entity(model) if model else None

    async def find_by_cnpj(self, cnpj: str) -> Optional[Campus]:
        async with self._session_factory() as session:

            stmt = (
                select(CampusModel)
                .where(CampusModel.cnpj == cnpj)
            )

            result = await session.execute(stmt)
            model = result.scalars().first()
            return CampusAdapter.model_to_entity(model) if model else None
