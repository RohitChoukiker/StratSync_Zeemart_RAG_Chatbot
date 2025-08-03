import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

class ExcelParser:
    def __init__(self, file_path: Path, chunk_size: int = 10):
        self.file_path = file_path
        self.chunk_size = chunk_size

    def parse(self) -> List[Dict[str, Any]]:
        """
        Parses all sheets in the Excel file and returns chunked, human-readable data.
        Each chunk contains metadata: sheet name, start row, end row, and text content.
        """
        parsed_chunks = []
        excel_data = pd.read_excel(self.file_path, sheet_name=None, engine="openpyxl")

        for sheet_name, df in excel_data.items():
            if df.empty:
                continue  # skip empty sheets

            # Clean the data
            df = df.dropna(how='all')  
            df.columns = df.columns.astype(str)  
            df.reset_index(drop=True, inplace=True)

            # Chunk the data
            for start in range(0, len(df), self.chunk_size):
                chunk_df = df.iloc[start:start + self.chunk_size]
                chunk_rows = chunk_df.to_dict(orient="records")

                # Make chunk human-readable
                text_lines = []
                for i, row in enumerate(chunk_rows):
                    line = ", ".join([f"{k}: {v}" for k, v in row.items()])
                    text_lines.append(f"Row {start + i + 1} - {line}")

                chunk_text = "\n".join(text_lines)

                parsed_chunks.append({
                    "sheet_name": sheet_name,
                    "start_row": int(start),
                    "end_row": int(start + len(chunk_df) - 1),
                    "content": chunk_text
                })

        return parsed_chunks
