import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

logger = logging.getLogger(__name__)

# Always use the current working directory as the base directory
BASE_DIR = Path.cwd()
logger.info(f"Using current working directory as base: {BASE_DIR}")

# Load .env from the base directory
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)
    logger.info(
        f"✅ Successfully loaded environment variables from: {env_path}")
else:
    logger.warning(f"⚠️ No .env file found at: {env_path}")
    logger.info(
        "Using default environment variables or system environment variables")


class PostgresSettings(BaseSettings):
    """PostgreSQL database settings"""

    model_config = ConfigDict(
        env_prefix="", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    user: str = Field(
        default="postgres", description="PostgreSQL username", env="POSTGRES_USER"
    )
    password: str = Field(
        default="", description="PostgreSQL password", env="POSTGRES_PASSWORD"
    )
    host: str = Field(
        default="localhost", description="PostgreSQL host", env="POSTGRES_HOST"
    )
    port: str = Field(
        default="5432", description="PostgreSQL port", env="POSTGRES_PORT"
    )
    db: str = Field(
        default="postgres", description="PostgreSQL database name", env="POSTGRES_DB"
    )
    connection_string: str = Field(
        default="",
        description="Full PostgreSQL connection string (if set, overrides individual settings)",
        env="POSTGRES_CONNECTION_STRING,SUPABASE_CONNECTION_STRING",
    )

    @property
    def get_connection_string(self) -> str:
        """Generate connection string if not explicitly provided"""
        if self.connection_string:
            return self.connection_string
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN")


settings = Settings()
