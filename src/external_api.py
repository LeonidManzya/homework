import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def convert_transaction(transaction):
    """Функция конвертации валюты в рубли"""

    currency_code = transaction["operationAmount"]["currency"]["code"]

    if currency_code == "RUB":
        return float(transaction["operationAmount"]["amount"])

    if currency_code in ("USD", "EUR"):
        try:
            amount = float(transaction["operationAmount"]["amount"])
            url = f"https://api.apilayer.com/currency_data/convert?to=RUB&from={currency_code}&amount={amount}"
            headers = {"apikey": API_KEY}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["result"]
        except Exception as e:
            print(f"Ошибка конвертации: {e}")
