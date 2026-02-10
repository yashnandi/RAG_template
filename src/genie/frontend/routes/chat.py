from fastapi import APIRouter
from genie.frontend.schemas import ChatRequest, ChatResponse, Source

from genie.rag.retriever import Retriever
from genie.rag.qa import RAGQA

RAG_GUARDRAIL_SUFFIX = (
    "\n\nReturn an answer which does not deviate too much from the context."
)

router = APIRouter()

# Instantiate once (like batch mode)
retriever = Retriever()
rag = RAGQA()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # 1) retrieve contexts (same as batch)
    ctxs = retriever.retrieve(req.query, top_k=req.top_k)

    # 2) run RAG answer
    answer = rag.answer(
        req.query + RAG_GUARDRAIL_SUFFIX,
        top_k=req.top_k,
    )

    return ChatResponse(
        answer=answer.strip(),
        sources=[
            Source(
                path=c.get("path", ""),
                score=float(c.get("score", 0.0)) if c.get("score") is not None else None,
                text=c.get("text", ""),
            )
            for c in ctxs
        ],
    )