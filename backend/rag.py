import numpy as np
from sentence_transformers import SentenceTransformer
from backend.vector_store import build_or_load_index
from backend.summarizer import ask_llm

model = SentenceTransformer("all-MiniLM-L6-v2")

def answer_question(question, top_k=5):
    index, chunks = build_or_load_index()

    if index is None or not chunks:
        return "No documents indexed yet."

    query_embedding = model.encode([question])
    distances, indices = index.search(query_embedding, top_k)

    retrieved_chunks = [chunks[i] for i in indices[0]]

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are an academic research assistant.

Answer the question strictly using the context below.
If the answer is not present, say "The answer is not found in the document."

Context:
{context}

Question:
{question}
"""

    return ask_llm(prompt)
