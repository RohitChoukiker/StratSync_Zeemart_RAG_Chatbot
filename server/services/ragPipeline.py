from typing import List
from server.services.vectorStore import VectorStore
from transformers import pipeline

class RAGPipeline:
    def __init__(self, vector_store: VectorStore, model_name: str = "google/flan-t5-base"):
        self.vector_store = vector_store
        self.qa_model = pipeline("text2text-generation", model=model_name)

    def build_prompt(self, query: str, context_chunks: List[dict]) -> str:
        """
        Combine the top chunks and query into a prompt for the model.
        """
        context_text = "\n\n".join([chunk["content"] for chunk in context_chunks])
        prompt = f"""You are an intelligent Excel assistant.

Given the following context from Excel:

{context_text}

Answer the following question:

{query}
"""
        return prompt

    def run(self, query: str, top_k: int = 5) -> str:
        """
        Full RAG pipeline: search -> build prompt -> call LLM -> return answer
        """
        
        context_chunks = self.vector_store.search(query, top_k=top_k)

        
        prompt = self.build_prompt(query, context_chunks)

        
        print(f"[RAGPipeline] Prompt:\n{prompt[:300]}...\n")
        result = self.qa_model(prompt, max_new_tokens=300, do_sample=False)
        
        return result[0]["generated_text"].strip()
