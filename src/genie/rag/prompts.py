# src/genie/rag/prompts.py

"""
Prompt helpers for Genie RAG assistant.
"""

SYSTEM_PROMPT = """
<YOUR PROMPT TEMPLATE>
"""


def build_prompt(context: str, question: str) -> str:
    """
    Build the user prompt by injecting RAG context and the user question
    into the template, along with scoring / behaviour instructions.
    """
    return f"""
Context:

{context}

Question:

{question}


"""
