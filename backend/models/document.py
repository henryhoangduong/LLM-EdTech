import json
from datetime import datetime
from typing import List

from core.database import Base
from langchain.schema import Document
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from models.henry_doc import HenryDoc


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class ChunkEmbedding(Base):
    """SQLAlchemy model for chunks_embeddings table"""

    __tablename__ = "chunks_embeddings"

    # Since LangChain Document uses string UUID, we'll use String type
    id = Column(String, primary_key=True, index=True)
    document_id = Column(
        String, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(String, nullable=False)
    data = Column(JSONB, nullable=False, default={})
    embedding = Column(Vector(384))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Define indexes using proper SQLAlchemy syntax
    __table_args__ = (
        # Index for faster user_id filtering
        # We'll create indexes separately in the ensure_text_search_index method
        {"schema": None}
    )

    # Relationship to parent document
    document = relationship("SQLDocument", back_populates="chunks")

    @classmethod
    def from_langchain_doc(
        cls, doc: Document, document_id: str, user_id: str, embedding: List[float]
    ) -> "ChunkEmbedding":
        """Create ChunkEmbedding from LangChain Document"""
        # Convert Document to dict format
        doc_dict = {"page_content": doc.page_content, "metadata": doc.metadata}

        return cls(
            id=doc.id,  # Use the LangChain document's ID directly as string
            document_id=document_id,
            user_id=user_id,
            data=json.loads(json.dumps(doc_dict, cls=DateTimeEncoder)),
            embedding=embedding,
        )

    def to_langchain_doc(self) -> Document:
        """Convert to LangChain Document"""
        return Document(
            page_content=self.data["page_content"], metadata=self.data["metadata"]
        )


class SQLDocument(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    data = Column(JSONB, nullable=False)
    chunks = relationship(
        "ChunkEmbedding", back_populates="document", cascade="all, delete-orphan"
    )

    @classmethod
    def from_henrydoc(cls, doc: HenryDoc, user_id: str) -> "SQLDocument":
        return cls(
            id=doc.id,
            user_id=user_id,
            data=json.loads(json.dumps(doc.dict(), cls=DateTimeEncoder)),
        )

    def to_henrydoc(self) -> HenryDoc:
        """Convert to SimbaDoc"""
        return HenryDoc(**self.data)
