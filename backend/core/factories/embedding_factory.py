import logging
from functools import lru_cache

from langchain.schema.embeddings import Embeddings
from langchain_community.embeddings import CohereEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings

from core.config import settings

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
    device = settings.embedding.device
    try:
        if settings.embedding.provider == "openai":
            return OpenAIEmbeddings(
                model=settings.embedding.model_name,
                **settings.embedding.additional_params,
                **kwargs,
            )
        elif settings.embedding.provider == "huggingface":
            return HuggingFaceEmbeddings(
                model_name=settings.embedding.model_name,
                # Use the potentially overridden device
                model_kwargs={"device": device},
                **settings.embedding.additional_params,
                **kwargs,
            )

        elif settings.embedding.provider == "ollama":
            return OllamaEmbeddings(
                model_name=settings.embedding.model_name or "nomic-embed-text",
                **settings.embedding.additional_params,
                **kwargs,
            )

        elif settings.embedding.provider == "cohere":
            return CohereEmbeddings(
                model=settings.embedding.model_name or "embed-english-v3.0",
                **settings.embedding.additional_params,
                **kwargs,
            )
    except Exception as e:
        logger.error(
            f"Error creating embeddings for provider {settings.embedding.provider}: {e}"
        )
        raise
