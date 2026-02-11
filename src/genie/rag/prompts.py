# src/genie/rag/prompts.py

"""
Prompt helpers for Genie RAG assistant.
"""

SYSTEM_PROMPT = """
Please suggest homeopathic remedies based on context pulled from materia medica which is a repository of homeopathic symptoms and remedies. 
Please give detailed course plan and instructions on using the medicine.
Add simple clear english explanation based on context. 

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
