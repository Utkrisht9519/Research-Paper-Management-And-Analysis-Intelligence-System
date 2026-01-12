from groq import Groq
from config import LLM_MODEL
from mcp.client.stdio import StdioClient

client = Groq()

# Connect to MCP server
mcp = StdioClient(["python", "mcp_server.py"])


def answer_query(query, paper_id=None):
    tools = {}

    # Semantic search always
    tools["context"] = mcp.call("semantic_search", {"query": query})

    # Wiki if asked
    if any(x in query.lower() for x in ["what is", "define", "explain", "wiki"]):
        term = query.split()[-1]
        tools["wiki"] = mcp.call("wiki_lookup", {"term": term})

    # Citations if asked
    if paper_id and any(x in query.lower() for x in ["cite", "reference", "source"]):
        tools["citations"] = mcp.call("citation_lookup", {"paper_id": paper_id})

    context = "\n".join(tools.get("context", []))

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
