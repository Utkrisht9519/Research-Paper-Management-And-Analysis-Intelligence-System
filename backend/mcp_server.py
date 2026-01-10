from backend.wiki_tool import wiki_lookup
from backend.citation_extractor import get_citations

TOOLS = {
    "wiki": wiki_lookup,
    "citations": get_citations
}

def call_tool(tool, arg):
    if tool not in TOOLS:
        raise ValueError("Tool not found")
    return TOOLS[tool](arg)
