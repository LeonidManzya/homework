import pandas as pd


def read_xlsx_file(file_path: str) -> list[dict]:
    """Функция чтения XLSX файла"""

    try:
        dikct_list = []
        df = pd.read_excel(file_path, dtype=str, engine="openpyxl")
        dikct_list.append(df.to_dict(orient="records"))
        return dikct_list
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")


print(read_xlsx_file("..\\data\\transactions_excel.xlsx"))
