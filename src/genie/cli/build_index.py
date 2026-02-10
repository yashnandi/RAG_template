from __future__ import annotations

import os
import json
from typing import List

import numpy as np

from genie.config import settings
from genie.ingest.pipeline import run_ingest
from genie.embeddings.embedder import Embedder
from genie.vectorstore.faiss_store import FaissStore


def _read_jsonl(path: str) -> List[dict]:
    rows: List[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def main() -> None:
    print("KB_PATH:", settings.kb_path)
    _, chunks_path = run_ingest()
    print("Chunks file:", chunks_path)

    # show exact line count first
    n_lines = sum(1 for _ in open(chunks_path, "r", encoding="utf-8"))
    print("Chunks lines:", n_lines)

    chunks = _read_jsonl(chunks_path)
    print("Chunks loaded:", len(chunks))

    if not chunks:
        raise RuntimeError(
            f"No chunks found in {chunks_path}. Put some files in knowledge_base/ first."
        )

    embedder = Embedder()
    texts = [c["text"] for c in chunks]

    vecs_list = []
    batch_size = 64
    for i in range(0, len(texts), batch_size):
        vecs_list.append(embedder.encode(texts[i : i + batch_size]))

    vectors = np.vstack(vecs_list).astype(np.float32)

    store = FaissStore.create(dim=vectors.shape[1])
    store.add(vectors, meta_rows=chunks)

    os.makedirs(settings.index_path, exist_ok=True)
    index_path = os.path.join(settings.index_path, "faiss.index")
    meta_path = os.path.join(settings.index_path, "meta.json")
    store.save(index_path, meta_path)

    print("✅ Index built successfully")
    print(f"- chunks: {len(chunks)}")
    print(f"- index:  {index_path}")
    print(f"- meta:   {meta_path}")


if __name__ == "__main__":
    main()
