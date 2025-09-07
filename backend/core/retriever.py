# core/retriever.py
from .embeddings import Embeddings
from .indexer import FaissIndexer
from typing import List, Dict, Any

class Retriever:
    def __init__(self, embedder: Embeddings, indexer: FaissIndexer):
        self.embedder = embedder
        self.indexer = indexer

    def retrieve(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        qvec = self.embedder.encode([query])
        hits = self.indexer.search(qvec, k=k)
        # return metadata + score
        out = []
        for score, meta in hits:
            m = meta.copy()
            m["score"] = score
            out.append(m)
        return out
