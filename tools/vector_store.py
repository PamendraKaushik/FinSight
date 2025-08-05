from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
index = None
texts = []

def build_store(docs):
    global index, texts
    texts = docs
    if not docs: return
    vectors = model.encode(docs)
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors))

def query_store(query):
    if not index: return ["No context available"]
    vec = model.encode([query])
    D, I = index.search(np.array(vec), k=3)
    return [texts[i] for i in I[0]]
