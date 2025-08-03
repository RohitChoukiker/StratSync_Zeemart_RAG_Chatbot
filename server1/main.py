# from fastapi import FastAPI, UploadFile, File
# from rag_chain import create_vectorstore_from_excel, answer_query
# import os

# app = FastAPI()

# os.makedirs("data", exist_ok=True)

# @app.post("/upload_excel/")
# async def upload_excel(file: UploadFile = File(...)):
#     path = f"data/{file.filename}"
#     with open(path, "wb") as f:
#         f.write(await file.read())
#     msg = create_vectorstore_from_excel(path)
#     return {"message": msg}

# @app.get("/ask/")
# def ask_question(q: str):
#     answer = answer_query(q)
#     return {"answer": answer}


from rag_chain import create_vectorstore_from_excel, answer_query

# STEP 1: Index Excel
file_path = "data/thisdata.xlsx"
print(create_vectorstore_from_excel(file_path))

# STEP 2: Ask a question
while True:
    question = input("\nAsk a question (or 'exit'): ")
    if question.lower() == "exit":
        break
    print("\nAnswer:", answer_query(question))
