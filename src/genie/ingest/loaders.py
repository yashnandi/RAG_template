from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Iterable
import hashlib

from pypdf import PdfReader


SUPPORTED_EXTS = {".txt", ".md", ".sql", ".sas", ".py", ".pdf"}


@dataclass(frozen=True)
class Document:
    doc_id: str
    path: str
    language: str
    text: str


def _stable_doc_id(path: Path) -> str:
    # stable id based on relative-ish path string
    h = hashlib.sha1(str(path).encode("utf-8")).hexdigest()
    return h[:16]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def _read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    out: List[str] = []
    for i, page in enumerate(reader.pages, start=1):
        txt = page.extract_text() or ""
        if txt.strip():
            out.append(f"\n--- PAGE {i} ---\n{txt}")
    return "\n".join(out)


def iter_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
            yield p


def load_doc(path: Path) -> Document:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTS:
        raise ValueError(f"Unsupported file type: {suffix} ({path})")

    if suffix == ".pdf":
        text = _read_pdf(path)
        language = "pdf"
    else:
        text = _read_text(path)
        language = suffix.lstrip(".")

    return Document(
        doc_id=_stable_doc_id(path),
        path=str(path).replace("\\", "/"),
        language=language,
        text=text,
    )


def load_docs(kb_path: str | Path) -> List[Document]:
    kb = Path(kb_path)
    docs: List[Document] = []
    for p in iter_files(kb):
        docs.append(load_doc(p))
    return docs
