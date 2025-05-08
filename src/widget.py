from src.masks import get_mask_account_number
from src.masks import get_mask_card_number


def mask_account_card(account_card: str) -> str | None:
    """Функция кодировки номера карты и счёта с применением функций масок."""

    name = ["Maestro", "MasterCard", "Visa Classic", "Visa Platinum", "Visa Gold"]
    number = []

    for i in account_card:
        if i.isdigit():
            number.append(i)

    for n in name:
        if n in account_card:
            return f"{n} {get_mask_card_number(''.join(number))}"
        elif "Счет" in account_card:
            return f"Счет {get_mask_account_number(''.join(number))}"


from datetime import datetime


def get_date(my_date: str) -> str:
    """Функция конвертирования даты"""
    date_formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%dT%H",
        "%Y-%m-%dT",
        "%Y-%m",
        "%Y",
        "%H:%M:%S.%f",
        "%M:%S.%f",
        "%S.%f",
        "%f",
    ]
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(my_date, fmt)
            return date_obj.strftime("%d.%m.%Y")
        except ValueError:
            continue
    raise ValueError("Неверный формат даты")
