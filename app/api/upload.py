from fastapi import APIRouter, UploadFile, File
from typing import List
from services.index_builder import build_index_from_csvs
import os

router = APIRouter()

@router.post("")
async def upload_csvs(files: List[UploadFile] = File(...)):
    result = await build_index_from_csvs(files)
    return result
