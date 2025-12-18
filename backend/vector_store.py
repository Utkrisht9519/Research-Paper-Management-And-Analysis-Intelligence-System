import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

INDEX_PATH = "data/index/faiss.index"
META_PATH = "data/index/chunks.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_or_load_index(chunks=None):
    if chunks is None and os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            stored_chunks = pickle.load(f)
        return index, stored_chunks

    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs("data/index", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(chunks, f)

    return index, chunks
