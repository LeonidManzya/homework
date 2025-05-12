import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs/masks.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты в виде числа и
    возвращает маску номера по правилу XXXX XX** **** XXXX"""

    if card_number.isdigit() and len(card_number) == 16:
        masked_number = card_number[0:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
        logger.info(f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}")
        return masked_number
    else:
        logger.error("Проверьте правильность введенного номера карты!")
        return "Проверьте правильность введенного номера карты!"


def get_mask_account_number(account_number: str) -> str:
    """Функция принимает на вход номер счёта в виде числа и
    возвращает маску номера по правилу **XXXX"""

    if account_number.isdigit() and len(account_number) == 20:
        masked_account = "**" + account_number[-4:]
        logger.info(f"** {account_number[-4:]}")
        return masked_account
    else:
        logger.error("Проверьте правильность введенного номера счёта!")
        return "Проверьте правильность введенного номера счёта!"


print(get_mask_card_number("9485213408774653"))
print(get_mask_account_number("84638237493322774455"))
