import os
import asyncio
from sqlalchemy import text
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

async def async_show_table() -> None:
    engine = create_async_engine(f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require", echo=True)
    async with engine.connect() as conn:
        result = await conn.execute(text('''SELECT table_name 
                                            FROM information_schema.tables 
                                            WHERE table_schema = 'public'
                                            AND table_type = 'BASE TABLE';'''))
        print(result.fetchall())
    await engine.dispose()

async def async_show_product() -> None:
    engine = create_async_engine(f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require", echo=True)
    async with engine.connect() as conn:
        result = await conn.execute(text('''SELECT * FROM product;'''))
        print(result.fetchall())
    await engine.dispose()

async def async_show_customer() -> None:
    engine = create_async_engine(f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require", echo=True)
    async with engine.connect() as conn:
        result = await conn.execute(text('''SELECT * FROM customer;'''))
        print(result.fetchall())
    await engine.dispose()

# asyncio.run(async_show_table())
# asyncio.run(async_show_product())
asyncio.run(async_show_customer())