import streamlit as st
from backend.pdf_parser import extract_text
from backend.vector_store import VectorStore
from backend.citation_extractor import extract_references, save_citations
from backend.rag_engine import answer_query
from backend.mcp_server import call_tool

st.title("📚 Research Paper Assistant")

uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type="pdf")

if uploaded_file:
    text = extract_text(uploaded_file)
    refs = extract_references(text)
    save_citations(uploaded_file.name, refs)

    vs = VectorStore()
    vs.build(text.split("\n"))

    st.success("Paper processed with citations tracked!")

    query = st.text_input("Ask a question")

    if query:
        chunks = vs.search(query)
        answer = answer_query(query, chunks)

        st.markdown("### Answer")
        st.write(answer)

        if "wiki" in query.lower():
            term = query.split()[-1]
            st.markdown("### Wiki Context")
            st.write(call_tool("wiki", term))

        st.markdown("### References")
        for r in refs[:5]:
            st.write("-", r)
