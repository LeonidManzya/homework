import json
import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def transactions(file_path: str) -> list[dict]:
    """Функция чтения json файла"""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            logger.error("JSON файл должен содержать список")
            raise ValueError("JSON файл должен содержать список")

        if data and not all(isinstance(item, dict) for item in data):
            logger.error("Список должен содержать только словари")
            raise ValueError("Список должен содержать только словари")

        logger.info("Файл открыт")
        return data

    except FileNotFoundError:
        logger.error("Файл не найден")
        raise FileNotFoundError(f"Файл не найден: {file_path}")


print(transactions(r"C:\Users\LM\PycharmProjects\PythonProject1\data\operations.json"))
