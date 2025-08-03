# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate
# from langchain_community.llms import HuggingFacePipeline
# from transformers import pipeline
# from loader_excel import load_excel_as_documents
# import os

# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")
# llm = HuggingFacePipeline(pipeline=qa_pipeline)

# custom_prompt = PromptTemplate(
#     template="""
#     You are a helpful assistant. Use the following context to answer the question.

#     Context:
#     {context}

#     Question:
#     {question}

#     Answer:
#     """,
#     input_variables=["context", "question"],
# )

# def create_vectorstore_from_excel(file_path: str):
#     documents = load_excel_as_documents(file_path)
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
#     docs = text_splitter.split_documents(documents)

#     vectorstore = FAISS.from_documents(docs, embedding=embedding_model)
#     vectorstore.save_local("faiss_store")
#     return "Index created successfully."

# def get_rag_qa_chain():
#     vectorstore = FAISS.load_local("faiss_store", embedding_model, allow_dangerous_deserialization=True)

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=retriever,
#         chain_type_kwargs={"prompt": custom_prompt}
#     )
#     return qa_chain

# def format_rag_answer(raw: str) -> str:
#     lines = raw.split(">10%")
#     formatted = []
#     for line in lines:
#         if not line.strip():
#             continue
#         parts = line.strip().split(",")
#         if len(parts) >= 6:
#             product = parts[2].replace('"', '').replace("Name: name", "").strip()
#             date = parts[3].strip()
#             new_price = parts[4].strip()
#             old_price = parts[5].strip()
#             formatted.append(
#                 f"Product: {product}\nDate: {date}\nOld Price: {old_price}\nNew Price: {new_price}\nDrop: >10%\n"
#             )
#     return "\n".join(formatted) if formatted else raw


# def answer_query(question: str) -> str:
#     chain = get_rag_qa_chain()
#     result = chain.invoke({"query": question})
#     raw = result["result"] if isinstance(result, dict) else result
#     return format_rag_answer(raw)




from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

from loader_excel import load_excel_as_documents
import os

# Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Lightweight LLM
qa_pipeline =  pipeline("text-generation", model="tiiuae/falcon-7b-instruct", trust_remote_code=True)
llm = HuggingFacePipeline(pipeline=qa_pipeline)

# Prompt 
custom_prompt = PromptTemplate(
    template="""
    You are a helpful assistant. Use the following context to answer the question.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """,
    input_variables=["context", "question"],
)

def create_vectorstore_from_excel(file_path: str):
    documents = load_excel_as_documents(file_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(docs, embedding=embedding_model)
    vectorstore.save_local("faiss_store")
    return "Index created successfully."

def get_rag_qa_chain():
    vectorstore = FAISS.load_local("faiss_store", embedding_model, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": custom_prompt}
    )
    return qa_chain

def format_rag_answer(raw: str) -> str:
    return raw.strip() if isinstance(raw, str) else str(raw)

def answer_query(question: str) -> str:
    chain = get_rag_qa_chain()
    result = chain.invoke({"query": question})
    raw = result["result"] if isinstance(result, dict) else result
    return format_rag_answer(raw)
