from mcp.server.fastmcp import FastMCP
import json
import os
import requests
from backend.vector_store import VectorStore
from config import CITATION_DB, WIKI_API

mcp = FastMCP("Research Assistant MCP")

# -----------------------------
# Semantic Search Tool
# -----------------------------
@mcp.tool()
def semantic_search(query: str):
    vs = VectorStore()
    vs.load()
    return vs.search(query, k=5)

# -----------------------------
# Wikipedia Tool
# -----------------------------
@mcp.tool()
def wiki_lookup(term: str):
    r = requests.get(WIKI_API + term)
    if r.status_code != 200:
        return "No wiki result found"
    return r.json().get("extract", "")

# -----------------------------
# Citation Tool
# -----------------------------
@mcp.tool()
def citation_lookup(paper_id: str):
    if not os.path.exists(CITATION_DB):
        return []
    with open(CITATION_DB) as f:
        data = json.load(f)
    return data.get(paper_id, [])

if __name__ == "__main__":
    mcp.run()
