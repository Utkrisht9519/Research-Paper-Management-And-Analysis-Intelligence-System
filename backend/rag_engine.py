from groq import Groq
from config import LLM_MODEL
from backend.vector_store import VectorStore
from backend.citation_extractor import get_citations
import requests

client = Groq()

def wiki_lookup(term):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{term}"
    r = requests.get(url)
    if r.status_code != 200:
        return ""
    return r.json().get("extract", "")

def semantic_search(query):
    vs = VectorStore()
    vs.load()
    return vs.search(query, k=5)

def answer_query(query, paper_id=None):
    tools = {}

    # Semantic search always
    tools["context"] = semantic_search(query)

    # Wiki if definition requested
    if any(x in query.lower() for x in ["what is", "define", "explain", "wiki"]):
        term = query.split()[-1]
        tools["wiki"] = wiki_lookup(term)

    # Citations if requested
    if paper_id and any(x in query.lower() for x in ["cite", "reference", "source"]):
        tools["citations"] = get_citations(paper_id)

    context = "\n".join(tools["context"])

    if "wiki" in tools:
        context += "\n\nWikipedia:\n" + tools["wiki"]

    if "citations" in tools:
        context += "\n\nCitations:\n" + "\n".join(tools["citations"][:5])

    prompt = f"""
You are a research assistant.
Use the context below to answer the question and cite sources.

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
