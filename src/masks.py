import logging
import os
from pathlib import Path

# Создаем папку logs рядом с src, если её нет
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(LOG_DIR / "masks.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает его маску"""
    if not isinstance(card_number, str):
        logger.error("Номер карты должен быть строкой")
        return "Проверьте правильность введенного номера карты!"

    card_number = card_number.replace(" ", "")

    if card_number.isdigit() and len(card_number) == 16:
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info(f"Успешная маскировка карты: {masked}")
        return masked
    logger.error(f"Неверный формат номера карты: {card_number}")
    return "Проверьте правильность введенного номера карты!"


def get_mask_account_number(account_number: str) -> str:
    """Функция принимает на вход номер счёта и возвращает его маску"""
    if not isinstance(account_number, str):
        logger.error("Номер счёта должен быть строкой")
        return "Проверьте правильность введенного номера счёта!"

    account_number = account_number.replace(" ", "")

    if account_number.isdigit() and len(account_number) == 20:
        masked = f"**{account_number[-4:]}"
        logger.info(f"Успешная маскировка счёта: {masked}")
        return masked
    logger.error(f"Неверный формат номера счёта: {account_number}")
    return "Проверьте правильность введенного номера счёта!"