"""Optional ChromaDB adapter for AEGIS AI vector storage."""

import os
from typing import Any


def get_chroma_collection(name: str = "aegis_documents") -> Any:
    """Return a local Chroma collection, creating it on first use."""
    import chromadb

    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./data/aegis_chroma")
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_or_create_collection(name=name)
