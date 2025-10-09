from typing import List, Optional

from langchain.schema import Document

from core.supabase_client import get_supabase_client
from services.retrieval.base import BaseRetriever
from services.vector_store.vector_store_service import VectorStoreService

supabase = get_supabase_client()


class DefaultRetriever(BaseRetriever):
    def __init__(
        self, vector_store: Optional[VectorStoreService] = None, k: int = 5, **kwargs
    ):
        super().__init__(vector_store)
        self.default_k = k

    def retrieve(self, query: str, user_id: str = None, **kwargs) -> List[Document]:
        user = supabase.auth.get_user()
        current_user_id = user.user.id

        return self.store.similarity_search(query, current_user_id)
