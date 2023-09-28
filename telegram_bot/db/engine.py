import logging

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData


def create_engine(url: URL) -> AsyncEngine:
    engine = create_async_engine(url, echo=False, pool_pre_ping=True)
    logging.info('Engine created')
    return engine


def get_session_pool(engine: AsyncEngine) -> sessionmaker:
    # noinspection PyTypeChecker
    session_pool = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    logging.info('Session pool created')
    return session_pool


async def proceed_schemas(metadata: MetaData, engine: AsyncEngine, debug: bool) -> None:
    async with engine.begin() as conn:
        if debug:
            logging.warning('RUNNING IN DEBUG MODE')
            # await conn.run_sync(metadata.drop_all)
            pass
        await conn.run_sync(metadata.create_all)
    logging.info('Created database')
