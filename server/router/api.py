from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from server.services.excelParser import ExcelParser
from server.services.vectorStore import VectorStore
from server.services.ragPipeline import RAGPipeline
import tempfile
from pathlib import Path

router = APIRouter()


vector_store = VectorStore()
rag_pipeline = RAGPipeline(vector_store=vector_store)

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    try:
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = Path(tmp.name)  

        
        parser = ExcelParser(file_path=tmp_path)

        
        chunks = parser.parse()

        
        vector_store.build_index(chunks)

        return {"status": "success", "chunks_indexed": len(chunks)}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/ask")
async def ask_question(query: str = Form(...)):
    try:
        answer = rag_pipeline.run(query)
        return {"query": query, "answer": answer}
    except Exception as e:
        return {"status": "error", "message": str(e)}
