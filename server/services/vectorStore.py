# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np
# from typing import List, Tuple, Dict, Any

# class VectorStore:
#     def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
#         self.model = SentenceTransformer(model_name)
#         self.index = None
#         self.chunk_metadata = []  

#     def build_index(self, chunks: List[Dict[str, Any]]):
#         """
#         Creates FAISS index from the list of chunks.
#         """
#         print("[VectorStore] Embedding", len(chunks), "chunks...")

        
#         texts = [chunk["content"] for chunk in chunks]

        
#         embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True).astype("float32")

        
#         dimension = embeddings.shape[1]
#         self.index = faiss.IndexFlatL2(dimension)
#         self.index.add(embeddings)

#         self.chunk_metadata = chunks

#     def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
#         """
#         Search top_k most relevant chunks for the user query.
#         """
#         query_embedding = self.model.encode([query], convert_to_numpy=True).astype("float32")
#         distances, indices = self.index.search(query_embedding, top_k)

#         results = []
#         for i in indices[0]:
#             if 0 <= i < len(self.chunk_metadata):
#                 results.append(self.chunk_metadata[i])
#         return results

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.chunks = []
        self.index = None

    def add_chunks(self, chunks: List[dict]):
        self.chunks = chunks
        embeddings = self.model.encode([chunk["content"] for chunk in chunks]).astype("float32")
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.embeddings = embeddings

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        query_embedding = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.chunks[i] for i in indices[0]]

