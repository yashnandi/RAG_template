import csv
import io
import json
import time
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse

from openai import OpenAI
from genie.config import settings
from genie.rag.retriever import Retriever
from genie.rag.qa import RAGQA

TOP_K = 3
SLEEP_SECS = 0.1
TEMPERATURE = 1 # do not change

BASELINE_SYSTEM = (
    "You are a helpful PySpark assistant. "
    "If you are unsure or lack information, say you don't know. "
    "Do not invent file paths, metrics, or code that you cannot justify."
)

RAG_GUARDRAIL_SUFFIX = (
    "\n\nReturn an answer which does not deviate too much from the context."
)

router = APIRouter()

retriever = Retriever()
rag = RAGQA()
client = OpenAI(api_key=settings.openai_api_key)


def format_sources(ctxs):
    parts = []
    for c in ctxs:
        path = str(c.get("path", "")).replace("\n", " ").strip()
        score = c.get("score")
        s = f"{float(score):.4f}" if score is not None else ""
        parts.append(f"{path}|{s}")
    return "; ".join(parts)


def simplify_contexts(ctxs):
    return [
        {
            "path": c.get("path", ""),
            "score": float(c.get("score", 0.0)) if c.get("score") is not None else None,
            "text": c.get("text", ""),
        }
        for c in ctxs
    ]


@router.post("/eval")
def run_eval(file: UploadFile = File(...)):
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY missing")

    contents = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(contents))

    out = io.StringIO()
    fieldnames = [
        "id",
        "category",
        "question",
        "rag_answer",
        "gpt_answer",
        "rag_sources",
        "rag_contexts",
        "rag_error",
        "gpt_error",
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
            "gpt_answer": "",
            "rag_sources": "",
            "rag_contexts": "",
            "rag_error": "",
            "gpt_error": "",
        }

        # ---------- RAG ----------
        try:
            ctxs = retriever.retrieve(question, top_k=TOP_K)
            result["rag_sources"] = format_sources(ctxs)
            result["rag_contexts"] = json.dumps(
                simplify_contexts(ctxs), ensure_ascii=False
            )

            rag_answer = rag.answer(
                question + RAG_GUARDRAIL_SUFFIX,
                top_k=TOP_K,
            )
            result["rag_answer"] = rag_answer.strip()
        except Exception as e:
            result["rag_error"] = repr(e)

        time.sleep(SLEEP_SECS)

        # ---------- Baseline GPT ----------
        try:
            resp = client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": BASELINE_SYSTEM},
                    {"role": "user", "content": question},
                ],
                temperature=TEMPERATURE,
            )
            result["gpt_answer"] = (
                resp.choices[0].message.content or ""
            ).strip()
        except Exception as e:
            result["gpt_error"] = repr(e)

        time.sleep(SLEEP_SECS)

        writer.writerow(result)

    out.seek(0)

    return StreamingResponse(
        out,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=rag_vs_gpt_eval.csv"
        },
    )