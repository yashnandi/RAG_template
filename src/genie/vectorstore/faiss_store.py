from __future__ import annotations

import os
import json
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import faiss


@dataclass
class FaissStore:
    dim: int
    index: faiss.Index
    meta: List[dict]

    @classmethod
    def create(cls, dim: int) -> "FaissStore":
        index = faiss.IndexFlatIP(dim)
        return cls(dim=dim, index=index, meta=[])

    def add(self, vectors: np.ndarray, meta_rows: List[dict]) -> None:
        assert vectors.dtype == np.float32
        assert vectors.ndim == 2 and vectors.shape[1] == self.dim
        self.index.add(vectors)
        self.meta.extend(meta_rows)

    def search(
        self, query_vec: np.ndarray, top_k: int = 6
    ) -> List[Tuple[float, dict]]:
        if query_vec.ndim == 1:
            query_vec = query_vec.reshape(1, -1)

        scores, ids = self.index.search(
            query_vec.astype(np.float32), top_k
        )

        results: List[Tuple[float, dict]] = []
        for s, i in zip(scores[0], ids[0]):
            if i == -1:
                continue
            results.append((float(s), self.meta[int(i)]))
        return results

    def save(self, index_path: str, meta_path: str) -> None:
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(self.index, index_path)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(
                {"dim": self.dim, "meta": self.meta},
                f,
                ensure_ascii=False,
                indent=2,
            )

    @classmethod
    def load(cls, index_path: str, meta_path: str) -> "FaissStore":
        index = faiss.read_index(index_path)
        with open(meta_path, "r", encoding="utf-8") as f:
            obj = json.load(f)
        return cls(dim=int(obj["dim"]), index=index, meta=obj["meta"])
