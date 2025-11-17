import asyncio
from datetime import datetime, timedelta
from random import uniform, randint
from sqlalchemy import text

from monitoring_backend.infra.databases.sqlalchemy.connection import Session, init_database
from monitoring_backend.infra.databases.sqlalchemy.models.air_conditioner import AirConditionerModel
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_unit import MonitoringUnitModel
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_payload import MonitoringPayloadModel
from monitoring_backend.infra.databases.sqlalchemy.models.monitoring_system_type import MonitoringSystemTypeModel


async def seed_database():
    """Popula o banco com dados iniciais de MonitoringSystemTypes, MonitoringUnits,
    AirConditioners e MonitoringPayloads.
    """

    # Inicializa o banco (com recriação opcional das tabelas)
    await init_database(drop_all=True)

    async with Session() as session:
        # Limpa todas as tabelas manualmente, se já existirem (ordem respeitando FKs)
        await session.execute(text("DELETE FROM monitoring_payloads CASCADE"))
        await session.execute(text("DELETE FROM air_conditioners CASCADE"))
        await session.execute(text("DELETE FROM monitoring_units CASCADE"))
        await session.execute(text("DELETE FROM monitoring_system_types CASCADE"))
        await session.commit()

        # Cria tipos de sistema
        system_types = [
            MonitoringSystemTypeModel(name="Climatização", description="Sensores de temperatura e umidade"),
            MonitoringSystemTypeModel(name="Energia", description="Medição de consumo elétrico"),
        ]
        session.add_all(system_types)
        await session.flush()  # garante que system_types tenham ids

        # Cria unidades de monitoramento vinculadas a um tipo de sistema
        monitoring_units = [
            MonitoringUnitModel(
                name="Unidade Campus A",
                identifier="MU-CAMPUS-A",
                monitoring_system_type_id=system_types[0].id,  # Climatização
            ),
            MonitoringUnitModel(
                name="Unidade Campus B",
                identifier="MU-CAMPUS-B",
                monitoring_system_type_id=system_types[0].id,  # Climatização
            ),
            MonitoringUnitModel(
                name="Unidade Laboratório",
                identifier="MU-LAB-01",
                monitoring_system_type_id=system_types[1].id,  # Energia
            ),
        ]
        session.add_all(monitoring_units)
        await session.flush()  # garante que monitoring_units tenham ids

        # Cria ar-condicionados associados a cada unidade
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
        await session.flush()

        # Cria payloads de monitoramento simulando leituras ao longo do tempo
        payloads = []
        for ac in air_conditioners:
            for i in range(10):  # 10 leituras por ar-condicionado
                payloads.append(
                    MonitoringPayloadModel(
                        monitoring_unit_id=ac.monitoring_unit_id,
                        air_conditioner_id=ac.id,
                        timestamp=datetime.utcnow() - timedelta(minutes=randint(0, 600)),
                        temperature=round(uniform(20.0, 28.0), 1),
                        humidity=round(uniform(40.0, 70.0), 1),
                        power_consumption=round(uniform(0.5, 2.5), 2),
                        voltage=[
                            round(uniform(110.0, 130.0), 2),
                            round(uniform(110.0, 130.0), 2),
                        ],
                        current=[
                            round(uniform(0.5, 20.0), 2),
                            round(uniform(0.5, 20.0), 2),
                        ],
                        extra_data={
                            "status": "ON" if randint(0, 1) else "OFF",
                            "fan_speed": randint(1, 5),
                        },
                    )
                )

        session.add_all(payloads)
        await session.commit()

    print("✅ Banco populado com sucesso! (SystemTypes + MonitoringUnits + AirConditioners + MonitoringPayloads)")


if __name__ == "__main__":
    asyncio.run(seed_database())
