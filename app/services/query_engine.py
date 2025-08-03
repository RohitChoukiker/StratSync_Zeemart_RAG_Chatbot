import pandas as pd
import os
import faiss
import numpy as np
from models.rag_models import embed_model, t5_tokenizer, t5_model

INDEX_PATH = "data/vector_index.faiss"
MAPPING_PATH = "data/index_mapping.csv"

def answer_query(question: str, top_k: int = 5):
    if not os.path.exists(INDEX_PATH) or not os.path.exists(MAPPING_PATH):
        return {"error": "❌ Please upload CSVs first."}

    index = faiss.read_index(INDEX_PATH)
    df = pd.read_csv(MAPPING_PATH)

    query_embedding = embed_model.encode([f"query: {question}"])
    distances, indices = index.search(np.array(query_embedding).astype("float32"), top_k)

    results = []
    for idx in indices[0]:
        if idx < len(df):
            results.append(df.iloc[idx]['text'])

    combined = "\n".join(results)
    prompt = f"Answer the question using below info.\nQuestion: {question}\nContext: {combined}"
    inputs = t5_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    output_ids = t5_model.generate(**inputs, max_new_tokens=100)
    answer = t5_tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return {
        "query": question,
        "matches": results,
        "answer": answer
    }
