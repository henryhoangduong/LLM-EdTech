import asyncio
import logging
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile
from langchain.schema import Document

from core.factories.storage_factory import StorageFactory
from models.henry_doc import HenryDoc, MetaDataType
from services.ingestion.loader import Loader
from services.splitting.splitter import Splitter
from services.storage.base import StorageProvider

logger = logging.getLogger(__name__)


class DocumentIngestionService:
    def __init__(self):
        self.loader = Loader()
        self.storage: StorageProvider = StorageFactory.get_storage_provider()
        self.splitter = Splitter()

    async def ingest_document(self, file: UploadFile, folder_path: str = "/"):
        try:
            file_path = Path(folder_path.strip("/"))/file.filename
            file_extension = f".{file.filename.split('.')[-1].lower()}"
            saved_local_path = await self.storage.save_file(file_path, file)
            saved_remote_path = await self.storage.get_public_url(file_path)
            file_size = file_path.stat().st_size
            if file_size == 0:
                raise ValueError(f"File {file_path} is empty")
            document = await self.loader.aload(file_path=str(file_path))
            document = await asyncio.to_thread(self.splitter.split_document, document)
            for doc in document:
                doc.id = str(uuid.uuid4())
            size_str = f"{file_size/(1024*1024):.2f} MB"
            metadata = MetaDataType(
                filename=file.filename,
                type=file_extension,
                page_number=len(document),
                chunk_number=0,
                enabled=False,
                parsing_status="Unparsed",
                size=size_str,
                loader=self.loader.__name__,
                uploadedAt=datetime.now().isoformat(),
                file_path=saved_remote_path,
                parser=None,
            )
            henrydoc = HenryDoc.from_documents(
                id=str(uuid.uuid4()), documents=document, metadata=metadata
            )
            return henrydoc
        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            raise e
