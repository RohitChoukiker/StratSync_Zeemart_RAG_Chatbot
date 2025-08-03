from typing import List
from server.services.vectorStore import VectorStore
from transformers import pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAGPipeline:
    def __init__(self, vector_store: VectorStore, model_name: str = "google/flan-t5-base"):
        self.vector_store = vector_store
        self.qa_model = pipeline("text2text-generation", model=model_name)

        # Safe chunking for prompt context
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,       # FLAN-T5 max token limit is 512, keep margin
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def build_prompt(self, query: str, context_chunks: List[dict]) -> str:
        """
        Combine the top chunks and query into a prompt for the model,
        while keeping it under token limits.
        """
        all_context_text = "\n\n".join([chunk["content"] for chunk in context_chunks])

        # ✅ Split long context safely
        split_contexts = self.splitter.split_text(all_context_text)

        # ✅ Keep only first few chunks to stay under token limit
        safe_context = "\n\n".join(split_contexts[:3])  # Adjust this as needed

        prompt = f"""You are an intelligent Excel assistant.

Given the following context from Excel:

{safe_context}

Answer the following question:

{query}
"""
        return prompt

    def run(self, query: str, top_k: int = 5) -> str:
        # ✅ Correct indenting
        context_chunks = self.vector_store.search(query, top_k=top_k)

        # ✅ Build prompt safely using text splitter
        prompt = self.build_prompt(query, context_chunks)

        print(f"[RAGPipeline] Prompt:\n{prompt[:300]}...\n")

        result = self.qa_model(prompt, max_new_tokens=300, do_sample=False)
        return result[0]["generated_text"].strip()
