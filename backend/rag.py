import numpy as np
from sentence_transformers import SentenceTransformer
from backend.vector_store import build_or_load_index
from backend.summarizer import ask_llm

model = SentenceTransformer("all-MiniLM-L6-v2")

def answer_question(question, top_k=10):
    index, chunks = build_or_load_index()

    if index is None or not chunks:
        return "No documents indexed yet."

    query_embedding = model.encode([question])
    distances, indices = index.search(query_embedding, top_k)

    retrieved_chunks = [chunks[i] for i in indices[0]]

    context = "\n\n".join(retrieved_chunks)

    prompt = prompt = f"""
You are an academic research assistant.

Your task is to ANSWER the question by:
- Understanding the provided context
- Summarizing and synthesizing relevant information
- Writing the answer in your OWN words in a clear, concise, academic tone

STRICT RULES:
- Use ONLY the information present in the context
- Do NOT copy sentences verbatim from the context
- Do NOT add external knowledge
- Do NOT infer beyond what is stated
- If the context does NOT contain enough information to answer the question, reply EXACTLY with:

"The answer is not found in the provided document context."

Context:
{context}

Question:
{question}

Answer (concise summary):
"""


    return ask_llm(prompt)
