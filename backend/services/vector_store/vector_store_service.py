import logging
import os
from typing import List, Optional

import faiss
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS

from core.config import settings

logger = logging.getLogger(__name__)


class VectorStoreService:
    def __init__(self, store=None, embeddings=None):
        self.store = store
        self.embeddings = embeddings
        if not store or not embeddings:
            raise ValueError("Both store and embeddings must be provided")

    def as_retriever(self, **kwargs):
        return self.store.as_retriever()
    
    def save(self):
        os.makedirs(settings.paths)