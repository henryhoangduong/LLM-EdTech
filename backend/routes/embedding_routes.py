from typing import List
from fastapi import APIRouter, HTTPException
from services.embedding.embedding_service import EmbeddingService
embedding_routes = APIRouter()
embeddingService = EmbeddingService()


@embedding_routes.post("/embed/documents")
async def embed_documents():
    pass


@embedding_routes.post("/embed/document/{doc_id}")
async def embed_document(doc_id: str):
    pass


@embedding_routes.get("/embedded_documents")
async def get_embedded_documents():
    pass


@embedding_routes.delete("/embed/document/chunk")
async def delete_document_chunk(chunk_ids: List[str]):
    pass


@embedding_routes.delete("/embed/document")
async def delete_document(doc_id: str):
    pass


@embedding_routes.delete("/embed/clear_store")
async def clear_store():
    pass
