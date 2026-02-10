from __future__ import annotations

import os
from typing import List, Dict

from genie.config import settings
from genie.embeddings.embedder import Embedder
from genie.vectorstore.faiss_store import FaissStore


class Retriever:
    def __init__(self):
        index_path = os.path.join(settings.index_path, "faiss.index")
        meta_path = os.path.join(settings.index_path, "meta.json")

        self.store = FaissStore.load(index_path, meta_path)
        self.embedder = Embedder()

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        query_vec = self.embedder.encode([query])[0]
        results = self.store.search(query_vec, top_k=top_k)

        out = []
        for score, meta in results:
            row = dict(meta)
            row["score"] = score
            out.append(row)
        return out
