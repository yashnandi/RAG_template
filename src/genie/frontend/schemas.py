from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str
    top_k: int = 3   # default matches batch TOP_K

class Source(BaseModel):
    path: str
    score: Optional[float]
    text: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]