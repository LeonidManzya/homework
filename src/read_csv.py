import pandas as pd


def read_csv_file(file_path: str) -> list[dict]:
    """Функция чтения csv файла"""

    try:
        dikct_list = []
        df = pd.read_csv(file_path, dtype=str)
        dikct_list.append(df.to_dict(orient="records"))
        return dikct_list
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")


print(read_csv_file(r"..\\data\\transactions.csv"))
