import pandas as pd
import os
import faiss
import uuid
import shutil
from typing import List
from fastapi import UploadFile
from sentence_transformers import SentenceTransformer
import numpy as np

UPLOAD_DIR = "data/uploaded_csvs"
INDEX_PATH = "data/vector_index.faiss"
MAPPING_PATH = "data/index_mapping.csv"

os.makedirs(UPLOAD_DIR, exist_ok=True)

embed_model = SentenceTransformer("intfloat/e5-small-v2")

async def build_index_from_csvs(files: List[UploadFile]):
    passages = []
    ids = []
    id_counter = 0

    for file in files:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            passage = " ".join([f"{col}: {str(row[col])}" for col in df.columns if pd.notnull(row[col])])
            formatted = f"passage: {passage}"
            passages.append(formatted)
            ids.append(id_counter)
            id_counter += 1

    embeddings = embed_model.encode(passages, batch_size=32, show_progress_bar=True, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    pd.DataFrame({"id": ids, "text": passages}).to_csv(MAPPING_PATH, index=False)

    return {"message": "✅ Index built", "rows_indexed": len(passages)}
