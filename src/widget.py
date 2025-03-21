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



print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 64686473678894779589"))
print(mask_account_card("MasterCard 7158300734726758"))
print(mask_account_card("Счет 35383033474447895560"))
print(mask_account_card("Visa Classic 6831982476737658"))
print(mask_account_card("Visa Platinum 8990922113665229"))
print(mask_account_card("Visa Gold 5999414228426353"))
print(mask_account_card("Счет 73654108430135874305"))


