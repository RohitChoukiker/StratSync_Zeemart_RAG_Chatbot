# import pandas as pd
# from langchain_core.documents import Document

# def load_excel_as_documents(file_path: str, chunk_size=500) -> list[Document]:
#     xls = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")
#     docs = []

#     for sheet_name, df in xls.items():
#         df = df.dropna(how='all')
#         csv_text = df.to_csv(index=False)
#         for i in range(0, len(csv_text), chunk_size):
#             chunk = csv_text[i:i+chunk_size]
#             metadata = {"sheet": sheet_name, "source": file_path}
#             docs.append(Document(page_content=chunk, metadata=metadata))

#     return docs


from typing import List
from langchain_core.documents import Document
import pandas as pd
import os

def load_excel_as_documents(file_path: str) -> List[Document]:
    documents = []
    excel_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")

    for sheet_name, df in excel_data.items():
        df.dropna(how="all", inplace=True)
        if df.empty:
            continue

        for _, row in df.iterrows():
            text = ", ".join([f"{col}: {str(row[col])}" for col in df.columns if pd.notna(row[col])])
            metadata = {"source": os.path.basename(file_path), "sheet": sheet_name}
            documents.append(Document(page_content=text, metadata=metadata))

    return documents

