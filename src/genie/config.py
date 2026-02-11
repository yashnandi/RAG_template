from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    llm_provider: str = os.getenv("GENIE_LLM_PROVIDER", "OPENAI").upper()

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    local_llm_model_path: str = os.getenv("LOCAL_LLM_MODEL_PATH", "")

    embed_model: str = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    kb_path: str = os.getenv("KB_PATH", "knowledge_base")
    data_path: str = os.getenv("DATA_PATH", "data")

    @property
    def processed_path(self) -> str:
        return os.path.join(self.data_path, "processed")

    @property
    def index_path(self) -> str:
        return os.path.join(self.data_path, "index")


settings = Settings()
