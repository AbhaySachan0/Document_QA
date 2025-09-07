# core/indexer.py
import faiss
import numpy as np
from typing import List, Dict, Any, Tuple, Optional

class FaissIndexer:
    def __init__(self, dim: int):
        self.dim = dim
        # index on Inner Product — use normalized vectors for cosine
        self.index = faiss.IndexFlatIP(dim)
        self._metadatas: List[Dict[str, Any]] = []

    def add(self, vectors: np.ndarray, metadatas: List[Dict[str, Any]]):
        """
        vectors: (N, dim) float32
        metadatas: length N list of dicts with info for each vector
        """
        if vectors.dtype != np.float32:
            vectors = vectors.astype("float32")
        # normalize for cosine similarity with inner product
        faiss.normalize_L2(vectors)
        self.index.add(vectors)
        self._metadatas.extend(metadatas)

    def search(self, query_vec: np.ndarray, k: int = 5) -> List[Tuple[float, Dict[str, Any]]]:
        """
        query_vec: (1, dim)
        returns list of (score, metadata) pairs
        """
        if query_vec.dtype != np.float32:
            query_vec = query_vec.astype("float32")
        faiss.normalize_L2(query_vec)
        D, I = self.index.search(query_vec, k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self._metadatas):
                continue
            results.append((float(score), self._metadatas[idx]))
        return results

    def count(self) -> int:
        return self.index.ntotal

    def all_metadata(self) -> List[Dict[str, Any]]:
        return list(self._metadatas)
