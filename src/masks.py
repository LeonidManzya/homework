def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты в виде числа и
    возвращает маску номера по правилу XXXX XX** **** XXXX"""

    if card_number.isdigit() and len(card_number) == 16:
        masked_number = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
        return masked_number
    else:
        return "Проверьте правильность введенного номера карты!"


def get_mask_account_number(account_number: str) -> str:
    """Функция принимает на вход номер счёта в виде числа и
    возвращает маску номера по правилу **XXXX"""

    if account_number.isdigit() and len(account_number) == 20:
        masked_account = "**" + account_number[-4:]
        return masked_account
    else:
        return "Проверьте правильность введенного номера счёта!"
