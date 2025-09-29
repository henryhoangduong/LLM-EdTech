import logging
from typing import Dict, List, Optional, Union, cast

from langchain.schema import Document

from core.factories.database_factory import get_database
from services.splitting.splitter import Splitter

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self.database = get_database()
        self.splitter = Splitter(chunk_size=5000, chunk_overlap=300)

    async def embed_all_documents(self) -> List[Document]:
        try:
            pass
        except Exception as e:
            logger.error(f"Error embedding all documents: {str(e)}")
            raise
