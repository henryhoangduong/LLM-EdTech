import logging
from enum import Enum
from functools import lru_cache
from typing import Optional

from core.config import settings
from database.postgres import PostgresDB

logger = logging.getLogger(__name__)


class DatabaseType(Enum):
    POSTGRES = "postgres"


SUPPORTED_DATABASES = {
    DatabaseType.POSTGRES: PostgresDB,
}

DEFAULT_DATABASE = DatabaseType.POSTGRES


@lru_cache()
def get_database(db_type: Optional[str] = None):
    try:
        db_type = db_type or settings.database.provider
        db_enum = DatabaseType(db_type.lower())

        if db_enum not in SUPPORTED_DATABASES:
            logger.warning(
                f"Unsupported database type: {db_type}, falling back to {DEFAULT_DATABASE.value}"
            )
            db_enum = DEFAULT_DATABASE

        db_class = SUPPORTED_DATABASES[db_enum]
        return db_class()
    except Exception as e:
        logger.error(
            f"Error creating database instance: {e}, falling back to {DEFAULT_DATABASE.value}"
        )
        return SUPPORTED_DATABASES[DEFAULT_DATABASE]()
