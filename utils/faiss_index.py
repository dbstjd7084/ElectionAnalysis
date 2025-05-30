import os
import faiss
import numpy as np

def load_faiss_index(index_path: str):
    index = faiss.read_index(index_path)
    ids = np.load(index_path.replace('.index', '_ids.npy'), allow_pickle=True)
    return index, ids

def search_faiss_index(index, query_embedding: list, top_k: int = 5):
    D, I = index.search(np.array([query_embedding]).astype('float32'), top_k)
    return I[0]
