# core/pipeline.py
from .document_loader import load_document
from .chunker import chunk_text
from .embeddings import Embeddings
from .indexer import FaissIndexer
from .retriever import Retriever
from .generator import Generator
from typing import List, Dict, Any
import numpy as np

class RAGPipeline:
    def __init__(self, embedding_model_name: str = None, openai_api_key: str = None):
        # initialize embedder
        self.embedder = Embeddings(model_name=embedding_model_name) if embedding_model_name else Embeddings()
        # infer dim from a sample
        sample = self.embedder.encode(["hello"])
        dim = sample.shape[1]
        self.indexer = FaissIndexer(dim=dim)
        self.retriever = Retriever(self.embedder, self.indexer)
        self.generator = Generator(api_key=openai_api_key)
        # we keep a local mapping of chunk text in metadata already in indexer._metadatas

    def ingest_bytes(self, filename: str, content_bytes: bytes, max_chunk_chars: int = 2000) -> int:
        mime, text = load_document(filename, content_bytes)
        chunks = chunk_text(text, max_chunk_chars=max_chunk_chars)
        if not chunks:
            return 0
        vectors = self.embedder.encode(chunks)
        metas: List[Dict[str, Any]] = []
        for i, c in enumerate(chunks):
            metas.append({"text": c, "source": filename, "chunk_id": i})
        # ensure numpy float32
        vectors = np.asarray(vectors, dtype="float32")
        self.indexer.add(vectors, metas)
        return len(chunks)

    def answer(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        hits = self.retriever.retrieve(question, k=top_k)
        # generator expects contexts with 'text' etc
        contexts = []
        for h in hits:
            contexts.append({
                "text": h.get("text") or h.get("text", ""),
                "source": h.get("source"),
                "chunk_id": h.get("chunk_id"),
                "score": h.get("score")
            })
        answer = self.generator.generate(question, contexts)
        return {"answer": answer, "contexts": contexts}
