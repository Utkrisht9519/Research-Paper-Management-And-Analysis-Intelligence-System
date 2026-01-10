import faiss, os, pickle
from sentence_transformers import SentenceTransformer
from config import VECTOR_DB_PATH, EMBEDDING_MODEL

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = faiss.IndexFlatL2(384)
        self.docs = []

    def build(self, texts):
        embeddings = self.model.encode(texts)
        self.index.add(embeddings)
        self.docs = texts

        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        faiss.write_index(self.index, f"{VECTOR_DB_PATH}/index.faiss")
        pickle.dump(self.docs, open(f"{VECTOR_DB_PATH}/docs.pkl", "wb"))

    def search(self, query, k=3):
        emb = self.model.encode([query])
        _, I = self.index.search(emb, k)
        return [self.docs[i] for i in I[0]]
