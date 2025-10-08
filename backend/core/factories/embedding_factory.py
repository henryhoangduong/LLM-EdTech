import logging
from functools import lru_cache

from core.config import settings
from langchain.schema.embeddings import Embeddings
from langchain_community.embeddings import CohereEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)

SUPPORTED_PROVIDERS = {
    "openai": OpenAIEmbeddings,
    "huggingface": HuggingFaceEmbeddings,
    "cohere": CohereEmbeddings,
}


@lru_cache()
def get_embeddings(**kwargs) -> Embeddings:
    if settings.embedding.provider not in SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported embedding provider: {settings.embedding.provider}. "
            f"Supported providers: {list(SUPPORTED_PROVIDERS.keys())}"
        )
    device=settings