from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData


def create_engine(url: URL) -> AsyncEngine:
    return create_async_engine(url, echo=True, pool_pre_ping=True)


def get_session_pool(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def proceed_schemas(session_pool: sessionmaker, metadata: MetaData, engine: AsyncEngine, debug: bool) -> None:
    
    async with engine.begin() as conn:
        if debug:
            await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
