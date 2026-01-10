"""
Minimal MCP-style tool registry
"""

from backend.wiki_tool import wiki_lookup
from backend.citation_extractor import get_citations

TOOLS = {
    "wiki": wiki_lookup,
    "citations": get_citations
}

def call_tool(tool_name, input_data):
    if tool_name not in TOOLS:
        raise ValueError("Tool not registered in MCP")
    return TOOLS[tool_name](input_data)
