import asyncio
from infra.databases.sqlalchemy.connection import test_connection

if __name__ == "__main__":
    asyncio.run(test_connection())
