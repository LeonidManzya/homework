import json
import logging
from pathlib import Path
from typing import List, Dict, Any


LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(
    LOG_DIR / "utils.log",
    mode="w",
    encoding="utf-8"
)
file_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_json(file_path: str) -> List[Dict[str, Any]]:

    try:
        logger.debug(f"Попытка чтения файла: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            error_msg = "JSON файл должен содержать список"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if data and not all(isinstance(item, dict) for item in data):
            error_msg = "Список должен содержать только словари"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"Успешно прочитано {len(data)} записей из {file_path}")
        return data

    except json.JSONDecodeError as e:
        error_msg = f"Ошибка парсинга JSON: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    except FileNotFoundError:
        error_msg = f"Файл не найден: {file_path}"
        logger.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"Неожиданная ошибка: {str(e)}"
        logger.error(error_msg)
        raise

print(read_json(r"C:\Users\LM\PycharmProjects\PythonProject1\data\operations.json"))