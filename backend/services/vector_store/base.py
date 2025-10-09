import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from langchain.docstore.document import Document
from langchain.schema.embeddings import Embeddings
from langchain.vectorstores import VectorStore

from core.factories.embedding_factory import get_embeddings

logger = logging.getLogger(__name__)


class VectorStoreBase(VectorStore):
    @property
    def embeddings(self) -> Optional[Embeddings]:
        """Access the query embedding object if available."""
        logger.debug(
            f"The embeddings property has not been "
            f"implemented for {self.__class__.__name__}"
        )
        return get_embeddings()

    @abstractmethod
    def from_texts(self, texts: List[str], **kwargs) -> List[str]:
        pass

    @abstractmethod
    def similarity_search(self, query: str, **kwargs) -> List[Document]:
        pass

    def as_retriever(self, **kwargs):
        pass

    def save(self):
        pass

    @abstractmethod
    def get_documents(self, document_ids: List[str]) -> List[Document]:
        """
        Get a document by its ID.

        Args:
            document_ids: The document IDs

        Returns:
            The documents
        """
        pass

    @abstractmethod
    def update_document(self, document_id: str, new_document: Document) -> bool:
        """
        Update a document in the store.

        Args:
            document_id: The document ID
            new_document: The new document

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def get_all_documents(self) -> List[Document]:
        """
        Get all documents from the store.

        Returns:
            List of documents
        """
        pass

    @abstractmethod
    def add_documents(self, documents: List[Document]) -> bool:
        """
        Add documents to the store.

        Args:
            documents: List of documents to add

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def delete_documents(self, uids: List[str]) -> bool:
        """
        Delete documents from the store.

        Args:
            uids: List of document IDs to delete

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def clear_store(self) -> bool:
        """
        Clear all documents from the store.

        Returns:
            True if successful, False otherwise
        """
        pass
