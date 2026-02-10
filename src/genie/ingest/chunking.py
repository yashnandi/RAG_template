from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    path: str
    language: str
    text: str
    start_char: int
    end_char: int


def chunk_text(
    doc_id: str,
    path: str,
    language: str,
    text: str,
    chunk_size: int = 900,
    overlap: int = 150,
) -> List[Chunk]:
    chunks: List[Chunk] = []
    n = len(text)
    i = 0
    idx = 0

    while i < n:
        j = min(i + chunk_size, n)
        piece = text[i:j]

        chunks.append(
            Chunk(
                chunk_id=f"{doc_id}_{idx}",
                doc_id=doc_id,
                path=path,
                language=language,
                text=piece,
                start_char=i,
                end_char=j,
            )
        )

        idx += 1
        if j == n:
            break

        i = max(0, j - overlap)

    return chunks
