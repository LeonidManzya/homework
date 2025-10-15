import re
import json
from typing import List, Dict, Any


def filter_transactions_by_description(
    transactions: List[Dict[str, Any]], search_pattern: str
) -> List[Dict[str, Any]]:
    try:
        pattern = re.compile(re.escape(search_pattern), re.IGNORECASE)  # Экранируем спецсимволы
    except re.error:
        return []

    filtered_transactions = []
    for transaction in transactions:
        description = transaction.get("description", "")
        if pattern.search(description):
            filtered_transactions.append(transaction)

    return filtered_transactions


if __name__ == "__main__":
    with open(r"C:\Users\LM\PycharmProjects\PythonProject1\data\operations.json", "r", encoding="utf-8") as file:
        transactions = json.load(file)  # Читаем JSON и преобразуем в список словарей

    filtered = filter_transactions_by_description(transactions, "открытие")
    print(filtered)
