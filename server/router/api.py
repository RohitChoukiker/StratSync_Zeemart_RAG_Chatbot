from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from server.services.excelParser import ExcelParser
from server.services.vectorStore import VectorStore
from server.services.ragPipeline import RAGPipeline
import tempfile

router = APIRouter()

# Global store (you can later replace with persistent or disk version)
vector_store = VectorStore()
rag_pipeline = RAGPipeline(vector_store=vector_store)

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # Step 1: Parse
        parser = ExcelParser()
        chunks = parser.parse_excel(tmp_path)

        # Step 2: Embed + Store
        vector_store.build_index(chunks)

        return {"status": "success", "chunks_indexed": len(chunks)}

    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/ask")
async def ask_question(query: str = Form(...)):
    """
    Ask a question based on the uploaded Excel
    """
    try:
        answer = rag_pipeline.run(query)
        return {"query": query, "answer": answer}

    except Exception as e:
        return {"status": "error", "message": str(e)}
