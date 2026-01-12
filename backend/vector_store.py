import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer
from config import VECTOR_DB_PATH, EMBEDDING_MODEL

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = None
        self.docs = []

    def build(self, texts):
        embeddings = self.model.encode(texts)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.docs = texts

        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        faiss.write_index(self.index, f"{VECTOR_DB_PATH}/index.faiss")
        pickle.dump(self.docs, open(f"{VECTOR_DB_PATH}/docs.pkl", "wb"))

    def load(self):
        index_path = f"{VECTOR_DB_PATH}/index.faiss"
        docs_path = f"{VECTOR_DB_PATH}/docs.pkl"

        if not os.path.exists(index_path) or not os.path.exists(docs_path):
            raise RuntimeError("Vector store not built yet")

        self.index = faiss.read_index(index_path)
        self.docs = pickle.load(open(docs_path, "rb"))

    def search(self, query, k=5):
        if self.index is None:
            self.load()

        emb = self.model.encode([query])
        _, I = self.index.search(emb, k)
        return [self.docs[i] for i in I[0]]
