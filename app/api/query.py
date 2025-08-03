from fastapi import APIRouter, Form
from services.query_engine import answer_query

router = APIRouter()

@router.post("")
async def query(question: str = Form(...), top_k: int = Form(5)):
    return answer_query(question, top_k)
