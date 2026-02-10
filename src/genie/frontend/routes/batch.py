import csv
import io
import json
import time
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse

from genie.rag.retriever import Retriever
from genie.rag.qa import RAGQA

TOP_K = 4
SLEEP_SECS = 0.2
RAG_GUARDRAIL_SUFFIX = (
    "\n\nReturn a direct answer. If the context is insufficient, say you don't know."
)

router = APIRouter()

retriever = Retriever()
rag = RAGQA()

def format_sources(ctxs):
    parts = []
    for c in ctxs:
        path = str(c.get("path", "")).replace("\n", " ").strip()
        score = c.get("score")
        s = f"{float(score):.4f}" if score is not None else ""
        parts.append(f"{path}|{s}")
    return "; ".join(parts)

@router.post("/batch")
def run_batch(file: UploadFile = File(...)):
    contents = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(contents))

    out = io.StringIO()
    fieldnames = [
        "id",
        "category",
        "question",
        "rag_answer",
        "rag_sources",
        "rag_contexts",
        "rag_error",
    ]
    writer = csv.DictWriter(out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        qid = row.get("id", "")
        cat = row.get("category", "")
        question = row.get("question", "")

        result = {
            "id": qid,
            "category": cat,
            "question": question,
            "rag_answer": "",
            "rag_sources": "",
            "rag_contexts": "",
            "rag_error": "",
        }

        try:
            ctxs = retriever.retrieve(question, top_k=TOP_K)
            result["rag_sources"] = format_sources(ctxs)
            result["rag_contexts"] = json.dumps(ctxs, ensure_ascii=False)

            answer = rag.answer(
                question + RAG_GUARDRAIL_SUFFIX,
                top_k=TOP_K,
            )
            result["rag_answer"] = answer.strip()

        except Exception as e:
            result["rag_error"] = repr(e)

        writer.writerow(result)
        time.sleep(SLEEP_SECS)

    out.seek(0)

    return StreamingResponse(
        out,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=rag_results.csv"
        },
    )