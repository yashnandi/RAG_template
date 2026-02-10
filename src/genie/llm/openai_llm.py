from __future__ import annotations

from openai import OpenAI

from genie.config import settings
from genie.llm.base import LLM


class OpenAILLM(LLM):
    def __init__(self):
        if not settings.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is missing. Add it to your .env file."
            )
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()},
            ],
            temperature=1,
        )
        return resp.choices[0].message.content.strip()
