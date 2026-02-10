from __future__ import annotations

import os
import json
from typing import List

from genie.config import settings
from genie.ingest.loaders import load_docs
from genie.ingest.chunking import chunk_text, Chunk


def _ensure_dirs() -> None:
    os.makedirs(settings.processed_path, exist_ok=True)
    os.makedirs(settings.index_path, exist_ok=True)


def _write_jsonl(path: str, rows: List[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_ingest() -> tuple[str, str]:
    _ensure_dirs()

    docs = load_docs(settings.kb_path)

    docs_path = os.path.join(settings.processed_path, "docs.jsonl")
    chunks_path = os.path.join(settings.processed_path, "chunks.jsonl")

    _write_jsonl(
        docs_path,
        [
            {
                "doc_id": d.doc_id,
                "path": d.path,
                "language": d.language,
                "text": d.text,
            }
            for d in docs
        ],
    )

    all_chunks: List[Chunk] = []
    for d in docs:
        all_chunks.extend(
            chunk_text(
                doc_id=d.doc_id,
                path=d.path,
                language=d.language,
                text=d.text,
            )
        )

    _write_jsonl(
        chunks_path,
        [
            {
                "chunk_id": c.chunk_id,
                "doc_id": c.doc_id,
                "path": c.path,
                "language": c.language,
                "text": c.text,
                "start_char": c.start_char,
                "end_char": c.end_char
            }
            for c in all_chunks
        ],
    )

    return docs_path, chunks_path