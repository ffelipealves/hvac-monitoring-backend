import asyncio
from sqlalchemy import text

from monitoring_backend.infra.databases.sqlalchemy.connection import Session, init_database
from monitoring_backend.infra.databases.sqlalchemy.models.air_conditioner import AirConditionerModel
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_unit import MonitoringUnitModel


async def seed_database():
    """Popula o banco com dados iniciais de MonitoringUnits e AirConditioners."""

    # Inicializa o banco (criação das tabelas etc.)
    await init_database(drop_all=True)

    async with Session() as session:
        # Limpa as tabelas (opcional, para evitar duplicação ao rodar o script várias vezes)
        await session.execute(text("DELETE FROM air_conditioners"))
        await session.execute(text("DELETE FROM monitoring_units"))
        await session.commit()

        # Cria unidades de monitoramento
        monitoring_units = [
            MonitoringUnitModel(name="Unidade Campus A", identifier="MU-CAMPUS-A"),
            MonitoringUnitModel(name="Unidade Campus B", identifier="MU-CAMPUS-B"),
            MonitoringUnitModel(name="Unidade Laboratório", identifier="MU-LAB-01"),
        ]

        session.add_all(monitoring_units)
        await session.flush()  # Garante que os IDs foram gerados antes de criar os A/Cs

        # Associa ar-condicionados a cada unidade
        air_conditioners = [
            # Unidade A
            AirConditionerModel(name="Samsung WindFree", monitoring_unit_id=monitoring_units[0].id),
            AirConditionerModel(name="LG Dual Inverter", monitoring_unit_id=monitoring_units[0].id),

            # Unidade B
            AirConditionerModel(name="Gree Eco Garden", monitoring_unit_id=monitoring_units[1].id),
            AirConditionerModel(name="Midea Luna", monitoring_unit_id=monitoring_units[1].id),

            # Unidade Laboratório
            AirConditionerModel(name="Daikin Inverter Pro", monitoring_unit_id=monitoring_units[2].id),
            AirConditionerModel(name="Philco Frio Turbo", monitoring_unit_id=monitoring_units[2].id),
            AirConditionerModel(name="Electrolux Turbo Max", monitoring_unit_id=monitoring_units[2].id),
        ]

        session.add_all(air_conditioners)
        await session.commit()

    print("✅ Banco populado com sucesso! (MonitoringUnits + AirConditioners)")


if __name__ == "__main__":
    asyncio.run(seed_database())
