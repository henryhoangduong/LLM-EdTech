import uuid
from typing import List, Optional

from langchain.schema import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Splitter:
    def __init__(self, strategy="recursive_character", chunk_size: int = 1500, chunk_overlap: int = 400):
        self.strategy = strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_document(self, documents: List[Document]) -> List[Document]:
        if not isinstance(documents, list) or not all(
            isinstance(doc, Document)for doc in documents
        ):
            raise ValueError(
                "Input must be a list of Langchain Document objects")
        if self.strategy == "recursive_character":
            return self.recursive_character_text_splitter(documents)
        elif self.strategy == "semantic_chunking":
            return self.semantic_chunking(documents)
        elif self.strategy == "markdown_header":
            return self.markdown_header_splitter(documents)
        elif self.strategy == "hierarchical":
            return self.hierarchical_splitter(documents)
        elif self.strategy == "context_aware":
            return self.context_aware_splitter(documents)
        else:
            raise ValueError(f"Invalid strategy: {self.strategy}")

    def recursive_character_text_splitter(
        self, documents: List[Document]
    ) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        documents = text_splitter.split_documents(documents)
        for doc in text_splitter.split_documents(documents):
            doc.id = str(uuid.uuid4())
        return documents
