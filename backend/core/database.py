import logging
import os
from collections.abc import AsyncGenerator

from fastapi.exceptions import ResponseValidationError
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)
url = URL.create(
    "postgresql+asyncpg",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
)
engine = create_async_engine(
    url,
    future=True,
    echo=True,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            raise
        except Exception as ex:
            if not isinstance(ex, ResponseValidationError):
                await logger.error(f"Database related error: {repr(ex)}")
            raise
