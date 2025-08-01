import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

class ExcelParser:
    def __init__(self, file_path: Path, chunk_size: int = 10):
        self.file_path = file_path
        self.chunk_size = chunk_size

    def parse(self) -> List[Dict[str, Any]]:
        """
        Parses all sheets in the Excel file and returns chunked data with metadata.
        """
        parsed_chunks = []

        
        excel_data = pd.read_excel(self.file_path, sheet_name=None, engine="openpyxl")

        for sheet_name, df in excel_data.items():
            if df.empty:
                continue  

            df = df.dropna(how='all')  
            df.columns = df.columns.astype(str)  
            df.reset_index(drop=True, inplace=True)

            
            for start in range(0, len(df), self.chunk_size):
                chunk_df = df.iloc[start:start+self.chunk_size]
                chunk_text = chunk_df.to_json(orient='records', force_ascii=False)

                parsed_chunks.append({
                    "sheet_name": sheet_name,
                    "start_row": int(start),
                    "end_row": int(start + len(chunk_df) - 1),
                    "content": chunk_text
                })

        return parsed_chunks
