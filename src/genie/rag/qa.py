from genie.rag.retriever import Retriever
from genie.rag.prompts import SYSTEM_PROMPT, build_prompt
from genie.llm.openai_llm import OpenAILLM

class RAGQA:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = OpenAILLM()

    def answer(self, question: str, top_k: int = 3) -> str:
        contexts = self.retriever.retrieve(question, top_k=top_k)
        prompt = build_prompt(question, contexts)
        return self.llm.generate(SYSTEM_PROMPT, prompt)
