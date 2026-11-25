import os
from typing import List
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document

QDRANT_DIR = "./qdrant_db"
COLLECTION_NAME = "gemma_docling_rag"

_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        _embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return _embeddings

def get_vectorstore():
    if os.path.exists(QDRANT_DIR) and os.listdir(QDRANT_DIR):
        client = QdrantClient(path=QDRANT_DIR)
        return QdrantVectorStore(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding=get_embeddings(),
        )
    return None

def salvar_no_qdrant(documents: List[Document]) -> QdrantVectorStore:
    return QdrantVectorStore.from_documents(
        documents=documents,
        embedding=get_embeddings(),
        path=QDRANT_DIR,
        collection_name=COLLECTION_NAME,
        force_recreate=False
    )