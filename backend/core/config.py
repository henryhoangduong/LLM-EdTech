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


class DatabaseConfig(BaseModel):
    provider: str = "litedb"
    additional_params: Dict[str, Any] = Field(default_factory=dict)


class LLMConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    provider: str = Field(default="openai")
    model_nam: str = Field(default="gpt-4")
    api_key: str = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", ""),
        description="OpenAI API key from environment variables",
    )
    base_url: str = Field(
        default="http://localhost:11434",
        description="Base URL for LLM service (e.g., Ollama server)",
    )
    temperature: float = Field(default=0.0)
    streaming: bool = Field(default=True)
    max_tokens: Optional[int] = None
    additional_params: Dict[str, Any] = Field(default_factory=dict)


class StorageSettings(BaseSettings):
    """Storage configuration settings"""
    provider: str = Field(
        default="local",
        description="Storage provider type: 'local', 'minio', or 'supabase'",
    )
    supabase_bucket: Optional[str] = Field(
        default="documents",
        description="Supabase storage bucket name",
        env="SUPABASE_STORAGE_BUCKET",
    )


class EmbeddingConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    provider: str = "openai"
    model_name: str = "text-embedding-3-small"
    device: str = os.getenv("DEVICE")

    additional_params: Dict[str, Any] = Field(default_factory=dict)


class VectorStoreConfig(BaseModel):
    provider: str = "faiss"
    collection_name: str = "migi_collection"
    additional_params: Dict[str, Any] = Field(default_factory=dict)


class ChunkingConfig(BaseModel):
    chunk_size: int = 50
    chunk_overlap: int = 50


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

    def __init__(self, **kwargs):
        env_values = {}
        for field_name, field in self.__class__.model_fields.items():
            env_var = (
                field.json_schema_extra.get(
                    "env") if field.json_schema_extra else None
            )
            if isinstance(env_var, str):
                env_vars = [env_var]
            elif isinstance(env_var, (list, tuple)):
                env_vars = env_var
            else:
                env_vars = []

            for var in env_vars:
                value = os.getenv(var)
                if value is not None:
                    env_values[field_name] = value
                    break
        env_values.update(kwargs)
        super().__init__(**env_values)


class FrontEndConfig(BaseModel):
    frontend_origin: str = Field(
        default="http://localhost:3000", description="Frontend url", env="FRONTEND_ORIGIN"
    )


class Settings(BaseSettings):
    postgres: PostgresSettings = PostgresSettings()
    frontend: FrontEndConfig = Field(default_factory=FrontEndConfig)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)

    @classmethod
    def load_from_yaml(cls, config_path: Optional[Path] = None) -> "Settings":
        config_file = BASE_DIR/"config.yaml"
        print("config_file: ", config_file)
        if not config_file.exists():
            raise FileNotFoundError(
                f"Config file not found at {config_file}. "
                "Please ensure config.yaml exists in the project root directory."
            )
        logger.info(f"Loading configuration from {config_file}")
        with open(config_file, "r") as f:
            config_data = yaml.safe_load(f) or {}
        return cls(**config_data)


settings = Settings.load_from_yaml()
