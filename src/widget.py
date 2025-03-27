from src.masks import get_mask_account_number, get_mask_card_number


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


def get_date(date_time: str) -> str:
    """Функция для преобразования даты и времени в формат ДД.ММ.ГГГГ"""
    return f"{date_time[8:10]}.{date_time[5:7]}.{date_time[:4]}"
