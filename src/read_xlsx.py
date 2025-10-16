import pandas as pd


def read_xlsx_file(file_path: str) -> list[dict]:
    """Функция чтения XLSX файла"""

    try:
        df = pd.read_excel(file_path, dtype=str, engine="openpyxl")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")