from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.router.api import router

app = FastAPI(
    title="Excel RAG Chatbot",
    description="Ask questions from your uploaded Excel files",
    version="1.0.0"
)


origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",
    "*"  
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
