import logging
import os
from pathlib import Path
from typing import Dict, Optional

from core.config import settings
from core.supabase_client import SupabaseClientSingleton
from fastapi import UploadFile
from services.storage.base import StorageProvider
from storage3.exceptions import StorageApiError
from supabase import Client

logger = logging.getLogger(__name__)


class SupabaseStorageProvider(StorageProvider):
    def __init__(self):
        self.client: Client = SupabaseClientSingleton.get_instance()
        self.bucket = settings.storage.supabase_bucket
        self.path_mapping: Dict[str, Path] = {}

    async def save_file(self, file_path: Path, file: UploadFile) -> Path:
        """Save a file to Supabase storage"""
        try:
            object_name = str(file_path).replace("\\", "/")

            # Upload to Supabase
            with open(file_path, "rb") as f:
                result = self.client.storage.from_(self.bucket).upload(
                    object_name, f, {"content-type": file.content_type}
                )

            # Reset file pointer for subsequent reads
            await file.seek(0)

            return file_path

        except Exception as e:
            logger.error(f"Error saving file to Supabase: {str(e)}")
            raise

    async def get_file(self, file_path: Path) -> Optional[bytes]:
        try:
            object_name = str(file_path).replace("\\", "/")
            response = self.client.storage.from_(
                self.bucket).download(object_name)
            return response
        except Exception as e:
            logger.error(f"Error retrieving file from Supabase: {str(e)}")
            return None

    async def delete_file(self, file_path):
        return await super().delete_file(file_path)

    async def file_exists(self, file_path):
        return await super().file_exists(file_path)

    async def get_public_url(self, file_path: Path) -> bool:
        try:
            object_name = str(file_path).replace("\\", "/")
            public_url = self.client.storage.from_(
                self.bucket).get_public_url(object_name)
            logger.info(
                f"Response after getting public url file supabase storage: {public_url}"
            )
            if public_url:
                return public_url[:-1]
            else:
                return None
        except Exception as e:
            logger.error(f"Error getting public url: {str(e)}")
            return False
