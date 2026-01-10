import streamlit as st
from backend.pdf_parser import extract_text
from backend.vector_store import VectorStore
from backend.citation_extractor import extract_references, save_citations
from backend.rag_engine import answer_query
from backend.mcp_server import call_tool

st.title("📚 Research Paper Assistant")

pdf = st.file_uploader("Upload PDF", type="pdf")

if pdf:
    text = extract_text(pdf)
    refs = extract_references(text)
    save_citations(pdf.name, refs)

    vs = VectorStore()
    vs.build(text.split("\n"))

    st.success("Paper processed")

    q = st.text_input("Ask a question")
    if q:
        ctx = vs.search(q)
        st.write(answer_query(q, "\n".join(ctx)))

        if "wiki" in q.lower():
            st.subheader("Wiki Context")
            st.write(call_tool("wiki", q.split()[-1]))

        st.subheader("References")
        for r in refs[:5]:
            st.write("-", r)
