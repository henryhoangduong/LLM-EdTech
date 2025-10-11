import json
import logging
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Any, List, Optional

import numpy as np
from langchain.schema.embeddings import Embeddings
from langchain.vectorstores import VectorStore
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from pgvector.sqlalchemy import Vector
from psycopg2.extras import RealDictCursor
from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from core.factories.embedding_factory import get_embeddings
from database.postgres import Base, DateTimeEncoder, PostgresDB, SQLDocument
from models.henry_doc import HenryDoc
from core.supabase_client import get_supabase_client
from models.document import ChunkEmbedding
supabase = get_supabase_client()

logger = logging.getLogger(__name__)


class PGVectorStore(VectorStore):
    """
    Custom PostgreSQL pgvector implementation using SQLAlchemy ORM.
    """

    def __init__(self, embedding_dim: int = 3072, create_indexes: bool = True):
        """
        Initialize the vector store.

        Args:
            embedding_dim: Dimension of the embedding vectors
            create_indexes: Whether to automatically create optimized indexes
        """
        self.embedding_dim = embedding_dim

        # Initialize PostgresDB if not already initialized
        self.db = PostgresDB()
        self._Session = self.db._Session

        # Initialize BM25 retriever as None, will be created on first use
        self._bm25_retriever = None
        self._bm25_docs = None

        # Log initialization
        logger.info("Vector store initialized")

    def get_document(self, document_id: str) -> Optional[HenryDoc]:
        """
        Retrieve a document from the store.

        Args:
            document_id: ID of the document to retrieve

        Returns:
            The retrieved document, or None if not found
        """
        session = None
        try:
            session = self._Session()
            doc = (
                session.query(SQLDocument).filter(
                    SQLDocument.id == document_id).first()
            )
            return doc.to_simbadoc() if doc else None
        finally:
            if session:
                session.close()

    @property
    def embeddings(self) -> Optional[Embeddings]:
        """Access the query embedding object if available."""
        logger.debug(
            f"The embeddings property has not been "
            f"implemented for {self.__class__.__name__}"
        )
        return get_embeddings()

    def add_documents(self, documents: List[Document], document_id: str) -> bool:
        """Add documents to the store using SQLAlchemy ORM."""
        session = None
        try:
            session = self._Session()

            # Check if document exists
            existing_doc = (
                session.query(SQLDocument).filter(
                    SQLDocument.id == document_id).first()
            )
            if not existing_doc:
                raise ValueError(f"Parent document {document_id} not found")

            # Get user_id from the document
            user_id = str(existing_doc.user_id)
            # Generate embeddings for all documents
            texts = [doc.page_content for doc in documents]
            embeddings = self.embeddings.embed_documents(texts)
            # Create ChunkEmbedding objects and explicitly set their IDs
            chunk_objects = []
            for doc, embedding in zip(documents, embeddings):
                chunk = ChunkEmbedding(
                    id=doc.id,  # Use the LangChain document's ID directly
                    document_id=document_id,
                    user_id=user_id,
                    data={"page_content": doc.page_content,
                          "metadata": doc.metadata},
                    embedding=embedding,
                )
                chunk_objects.append(chunk)
            # Add all chunks to session
            session.add_all(chunk_objects)
            session.commit()

            logger.info(
                f"Successfully added {len(documents)} chunks for document {document_id}"
            )
            return True

        except Exception as e:
            if session:
                session.rollback()
            logger.error(f"Failed to add documents: {e}")
            raise  # Re-raise the exception to handle it at a higher level
        finally:
            if session:
                session.close()

    def get_all_documents(self, user_id: str) -> List[Document]:
        """Get all documents from the store, optionally filtered by user_id."""
        session = None
        try:
            session = self._Session()
            query = session.query(ChunkEmbedding)
            chunks = query.all()
            # Modify this to ensure document_id is in metadata
            return [
                Document(
                    page_content=chunk.data["page_content"],
                    metadata={
                        **chunk.data.get("metadata", {}),
                        "document_id": chunk.document_id,  # Explicitly add document_id
                    },
                )
                for chunk in chunks
            ]
        finally:
            if session:
                session.close()

    def _retrieve_with_bm25(self, query: str, user_id: str, k: int = 30) -> List[str]:
        """
        Perform first-pass BM25 retrieval to get candidate document IDs.

        Args:
            query: Search query
            user_id: User ID for filtering
            k: Number of documents to retrieve

        Returns:
            List of document IDs from BM25 retrieval
        """
        # Get BM25 retriever (will be cached after first use)
        bm25_retriever = self._get_bm25_retriever(user_id, k)

        # Get top documents using BM25
        first_pass_docs = bm25_retriever.get_relevant_documents(query)
        logger.debug(f"BM25 returned {len(first_pass_docs)} documents")

        # Extract document IDs from first pass results
        first_pass_doc_ids = list(
            {doc.metadata["document_id"] for doc in first_pass_docs}
        )

        return first_pass_doc_ids

    def _retrieve_with_text_search(
        self,
        query: str,
        top_k: int,
        document_ids: Optional[List[str]] = None,
        language: str = "french",
    ) -> List[Document]:
        """
        Perform text-based search using PostgreSQL's full-text search.

        Args:
            query: Search query
            user_id: User ID for filtering
            top_k: Number of results to retrieve
            document_ids: Optional list of document IDs to filter by
            language: Language for text search

        Returns:
            List of Document objects with results
        """
        session = None
        try:
            # Get a session and its engine
            session = self._Session()
            conn = session.connection()
            cur = conn.connection.cursor(cursor_factory=RealDictCursor)

            # Prepare the SQL query for text search
            sql = """
                SELECT * FROM chunks_embeddings 
                WHERE  
            """

            params = []

            if document_ids:
                sql += " document_id = ANY(%s) "
                params.append(document_ids)

            sql += f"""
                ORDER BY ts_rank(to_tsvector(%s, data->>'page_content'), 
                               plainto_tsquery(%s, %s)) DESC
                LIMIT %s
            """
            params.extend([language, language, query, top_k])

            # Execute query
            cur.execute(sql, params)
            rows = cur.fetchall()

            # Convert rows to Document objects
            results = []
            for row in rows:
                # Create a document with the data from the row
                doc = Document(
                    page_content=row["data"].get("page_content", ""),
                    metadata={
                        **row["data"].get("metadata", {}),
                        "id": row["id"],
                        "document_id": row["document_id"],
                    },
                )
                results.append(doc)

            return results

        finally:
            if session:
                session.close()

    def _fuse_results_rrf(
        self, *ranked_lists: List[Document], k: int = 60, top_k: int = 100
    ) -> List[Document]:
        """
        Fuse multiple result lists using Reciprocal Rank Fusion.

        Args:
            ranked_lists: Multiple lists of Documents in rank order
            k: RRF constant (default=60)
            top_k: Number of results to return after fusion

        Returns:
            List of fused Document objects
        """
        # Create a mapping from document ID to document object
        doc_map = {}

        # Calculate RRF scores
        scores = defaultdict(float)
        for lst in ranked_lists:
            for rank, doc in enumerate(lst, start=1):
                doc_id = doc.metadata.get("id")
                if doc_id is None:
                    continue

                # Store document for later retrieval
                doc_map[doc_id] = doc

                # Add RRF score
                scores[doc_id] += 1 / (k + rank)

        # Sort by score and get top_k document IDs
        top_ids = [
            d for d, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)
        ][:top_k]

        # Return documents in the new fused order
        return [doc_map[doc_id] for doc_id in top_ids if doc_id in doc_map]

    def _retrieve_with_dense_vector(
        self,
        query: str,
        top_k: int,
        document_ids: Optional[List[str]] = None,
    ) -> List[Document]:
        """
        Perform pure vector similarity search.

        Args:
            query: Search query
            user_id: User ID for filtering
            top_k: Number of results to retrieve
            document_ids: Optional list of document IDs to filter by (from BM25)

        Returns:
            List of Document objects with results
        """
        session = None
        try:
            # Get a session and its engine
            session = self._Session()
            conn = session.connection()
            cur = conn.connection.cursor(cursor_factory=RealDictCursor)

            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            query_embedding_array = np.array(query_embedding)
            # Convert numpy array to list for psycopg2
            query_embedding_list = query_embedding_array.tolist()
            # Prepare the SQL query
            sql = """
                SELECT * FROM chunks_embeddings 
            """

            params = []
            if document_ids:
                sql += "WHERE document_id = ANY(%s) "
                params.append(document_ids)

            sql += """
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """
            params.extend([query_embedding_list, top_k])

            # Execute query
            cur.execute(sql, params)
            rows = cur.fetchall()

            # Convert rows to Document objects
            results = []
            for row in rows:
                # Create a document with the data from the row
                doc = Document(
                    page_content=row["data"].get("page_content", ""),
                    metadata={
                        **row["data"].get("metadata", {}),
                        "id": row["id"],
                        "document_id": row["document_id"],
                    },
                )
                results.append(doc)

            return results

        finally:
            if session:
                session.close()

    def _get_bm25_retriever(self, user_id: str, k: int = 10) -> BM25Retriever:
        """
        Get or create BM25 retriever for a user.
        Caches the retriever and documents to avoid rebuilding for each query.
        """
        if self._bm25_retriever is None or self._bm25_docs is None:
            # Get all documents for this user
            self._bm25_docs = self.get_all_documents(user_id=user_id)
            logger.debug(
                f"Initialized BM25 with {len(self._bm25_docs)} documents")

            # Initialize BM25 retriever
            self._bm25_retriever = BM25Retriever.from_documents(
                self._bm25_docs,
                k=k,
                bm25_params={
                    "k1": 1.2,
                    "b": 0.75,
                },
            )

        return self._bm25_retriever

    def similarity_search(
        self,
        query: str,
        user_id: str = "1",
        top_k: int = 200,
        bm25_k: int = 100,
        dense_k: int = 100,
        use_bm25_first_pass: bool = True,
        language: str = "french",
    ) -> List[Document]:
        """
        Search for documents similar to a query, filtered by user_id.
        Uses a fusion of BM25 and dense retrieval results.

        Args:
            query: The search query
            user_id: The user ID to filter results by
            top_k: The number of top results to return after fusion (default: 200)
            bm25_k: Number of results to retrieve from BM25 (default: 100)
            dense_k: Number of results to retrieve from dense vectors (default: 100)
            use_bm25_first_pass: Whether to use BM25 retrieval
            language: The language to use for text search (default: 'french')

        Returns:
            A list of documents similar to the query
        """
        # Step 1: Sparse BM25 retrieval
        sparse_results = []
        if use_bm25_first_pass:
            # Get document IDs from BM25
            bm25_doc_ids = self._retrieve_with_bm25(query, user_id, bm25_k)
            # Get actual documents from database with text search ranking
            sparse_results = self._retrieve_with_text_search(
                query=query,
                top_k=bm25_k,
                document_ids=bm25_doc_ids,
                language=language,
            )

        # Step 2: Dense vector retrieval
        dense_results = self._retrieve_with_dense_vector(
            query=query,
            top_k=dense_k,
            document_ids=None,  # Don't filter by BM25 results for pure dense retrieval
        )

        # Step 3: Fuse results using RRF
        if use_bm25_first_pass and sparse_results:
            fused_results = self._fuse_results_rrf(
                sparse_results, dense_results, k=60, top_k=top_k
            )
        else:
            # If no BM25, just use dense results
            fused_results = dense_results[:top_k]

        # Return fused results
        return fused_results

    def from_texts(
        self,
        texts: List[str],
        embedding: Optional[Embeddings] = None,
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[str]:
        """Add texts to the vector store.

        Args:
            texts: List of texts to add
            embedding: Optional embedding function (will use self.embeddings if not provided)
            metadatas: Optional list of metadatas associated with the texts
            ids: Optional list of IDs to associate with the texts
            **kwargs: Additional arguments (must include document_id)

        Returns:
            List of IDs of the added texts
        """
        session = None
        try:
            session = self._Session()

            # Get document_id from kwargs
            document_id = kwargs.get("document_id")
            if not document_id:
                raise ValueError("document_id is required in kwargs")

            # Check if document exists
            existing_doc = (
                session.query(SQLDocument).filter(
                    SQLDocument.id == document_id).first()
            )
            if not existing_doc:
                raise ValueError(f"Parent document {document_id} not found")

            # Get user_id from the document
            user_id = existing_doc.user_id

            # Use provided embeddings or default to self.embeddings
            embeddings_func = embedding or self.embeddings

            # Generate embeddings
            embeddings = embeddings_func.embed_documents(texts)

            # Handle metadata
            if not metadatas:
                metadatas = [{} for _ in texts]

            # Handle IDs
            if not ids:
                ids = [str(uuid.uuid4()) for _ in texts]

            # Create chunk objects
            chunk_objects = []
            for text, metadata, embedding_vector, chunk_id in zip(
                texts, metadatas, embeddings, ids
            ):
                chunk = ChunkEmbedding(
                    id=chunk_id,
                    document_id=document_id,
                    user_id=user_id,
                    data={"page_content": text, "metadata": metadata},
                    embedding=embedding_vector,
                )
                chunk_objects.append(chunk)

            # Add all chunks to session
            session.add_all(chunk_objects)
            session.commit()

            logger.info(
                f"Successfully added {len(texts)} texts for document {document_id}"
            )
            return ids

        except Exception as e:
            if session:
                session.rollback()
            logger.error(f"Failed to add texts: {e}")
            raise
        finally:
            if session:
                session.close()

    def delete_documents(self, doc_id: str) -> bool:
        session = None
        try:
            user_id = supabase.auth.get_user().user.id
            doc = (
                session.query(SQLDocument)
                .filter(SQLDocument.id == doc_id, SQLDocument.user_id == user_id)
                .first()
            )
            if not doc:
                raise ValueError(
                    f"User {user_id} does not have access to document {doc_id}"
                )
            query = session.query(ChunkEmbedding).filter(
                ChunkEmbedding.document_id == doc_id
            )
            deleted_count = query.delete(synchronize_session=False)
            session.commit()

            logger.info(f"Successfully deleted {deleted_count} chunks")
            return True
        except Exception as e:
            logger.error(f"Failed to delete documents: {e}")
            if session:
                session.rollback()
            return False
        finally:
            if session:
                session.close()
