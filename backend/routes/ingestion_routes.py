import asyncio
import logging
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from core.database import get_db
from middleware.auth import get_current_user
from services.ingestion.ingestion_service import DocumentIngestionService

logger = logging.getLogger(__name__)
ingestion_routes = APIRouter()

db = get_db()
ingestion_service = DocumentIngestionService()


@ingestion_routes.post("")
async def ingest_document(
        files: List[UploadFile] = File(...),
    folder_path: str = Query(
        default="/", description="Folder path to store the document"
            ),
):
    """Ingest a document into the vector store"""
    try:
        print("files: ", files)

        async def process_file(file):
            henry_doc = await ingestion_service.ingest_document(file, folder_path)
            return henry_doc
        response = await asyncio.gather(*[process_file(file) for file in files])
        return response
    except Exception as e:
        logger.error(f"Error in ingest_document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@ingestion_routes.get("/ingestion")
async def get_ingestion_documents():
    """Get all ingested documents for the current user"""
    pass
