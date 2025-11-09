# connection.py

from collections.abc import AsyncGenerator
from decouple import config
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text

from monitoring_backend.infra.databases.sqlalchemy.models.base import Base

url = URL.create(
    drivername=config("DATABASE_DRIVER"),
    username=config("DATABASE_USER"),
    password=config("DATABASE_PASSWORD"),
    host=config("DATABASE_HOST"),
    port=config("DATABASE_PORT"),
    database=config("DATABASE_NAME"),
)

engine = create_async_engine(url, echo=True)
Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_database(drop_all: bool = False):
    async with engine.begin() as conn:
        if drop_all:
            print("⚠️  Limpando todas as tabelas do banco antes de criar novamente...")
            # Deleta todas as tabelas no banco
            await conn.run_sync(Base.metadata.drop_all)

        # Cria novamente todas as tabelas do projeto
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Banco de dados inicializado com sucesso!")

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session
        

async def test_connection():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Conexão com o banco bem-sucedida!")
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
