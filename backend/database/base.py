from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from models.henry_doc import HenryDoc


class DatabaseService(ABC):
    @abstractmethod
    def insert_document(self, document: HenryDoc) -> str:
        pass

    @abstractmethod
    def insert_documents(self, documents: List[HenryDoc]) -> List[str]:
        pass

    @abstractmethod
    def get_document(self, document_id: str) -> Optional[HenryDoc]:
        pass

    @abstractmethod
    def get_all_documents(self) -> List[HenryDoc]:
        pass

    @abstractmethod
    def update_document(self, document_id: str, document: HenryDoc) -> bool:
        pass

    @abstractmethod
    def delete_document(self, document_id: str) -> bool:
        pass

    @abstractmethod
    def delete_documents(self, document_ids: List[str]) -> bool:
        pass

    @abstractmethod
    def clear_database(self) -> bool:
        pass

    @abstractmethod
    def query_documents(self, filters: Dict[str, Any]) -> List[HenryDoc]:
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Union[bool, str]]:
        pass
