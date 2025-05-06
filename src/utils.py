import json


def transactions(file_path: str) -> list[dict]:
    """Функция чтения json файла"""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("JSON файл должен содержать список")

        if data and not all(isinstance(item, dict) for item in data):
            raise ValueError("Список должен содержать только словари")

        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")
