# core/embeddings.py
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import os

MODEL_NAME = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")

class Embeddings:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Returns numpy array of shape (len(texts), dim)
        """
        vecs = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return vecs
