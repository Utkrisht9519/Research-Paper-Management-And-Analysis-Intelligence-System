import streamlit as st
import os

from backend.pdf_parser import parse_pdf
from backend.chunking import chunk_text
from backend.vector_store import build_or_load_index
from backend.rag import answer_question

st.set_page_config(page_title="GA03 Research Assistant")

st.title("📚 GA03 Research Paper Assistant")

uploaded = st.file_uploader("Upload a research paper (PDF)", type="pdf")

if uploaded:
    os.makedirs("data/papers", exist_ok=True)
    path = f"data/papers/{uploaded.name}"

    with open(path, "wb") as f:
        f.write(uploaded.read())

    text = parse_pdf(path)

    if text.strip():
        st.success("PDF parsed successfully.")

        # Remove references section before chunking
        lower_text = text.lower()
        if "references" in lower_text:
            text = text[: lower_text.rfind("references")]

        chunks = chunk_text(text)

        build_or_load_index(chunks)

        st.success(f"Indexed {len(chunks)} chunks into FAISS.")

        with st.expander("Preview extracted text"):
            st.text_area("Text preview", text[:2000], height=300)

        st.markdown("---")
        st.subheader("Ask a question about this paper")

        question = st.text_input("Your question")

        if question:
            with st.spinner("Thinking..."):
                answer = answer_question(question)
            st.markdown("### Answer")
            st.write(answer)

    else:
        st.warning(
            "No extractable text found. "
            "This PDF appears to be scanned or image-based."
        )
