def extract_metadata(df, sheet_name, row_index):
    return {
        "sheet": sheet_name,
        "row": row_index,
        "columns": list(df.columns)
    }