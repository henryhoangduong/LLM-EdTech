from typing import Dict, Type

from core.config import settings
from services.storage.base import StorageProvider
from services.storage.supabase_storage import SupabaseStorageProvider


class StorageFactory:
    _providers: Dict[str, Type[StorageProvider]] = {
        "supabase": SupabaseStorageProvider,
    }

    @classmethod
    def get_storage_provider(cls) -> StorageProvider:
        """Get the configured storage provider

        Returns:
            StorageProvider: The configured storage provider instance
        """
        provider_type = settings.storage.provider.lower()
        if provider_type not in cls._providers:
            raise ValueError(f"Unknown storage provider: {provider_type}")

        provider_class = cls._providers[provider_type]
        return provider_class()
