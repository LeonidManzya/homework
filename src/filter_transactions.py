import re
import json
from typing import List, Dict, Any


def filter_transactions_by_description(
        transactions: List[Dict[str, Any]],
        search_pattern: str
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по описанию (через регулярное выражение).

    Args:
        transactions: Список словарей с транзакциями.
        search_pattern: Регулярное выражение для поиска в поле "description".

    Returns:
        Список транзакций, где описание совпадает с `search_pattern`.
    """
    try:
        pattern = re.compile(search_pattern, re.IGNORECASE)
    except re.error:
        return []

    filtered_transactions = []
    for transaction in transactions:
        description = transaction.get("description", "")
        if pattern.search(description):
            filtered_transactions.append(transaction)

    return filtered_transactions


if __name__ == "__main__":
    # Загрузка данных из JSON-файла
    with open('data/operations.json', 'r', encoding='utf-8') as file:
        transactions = json.load(file)  # Предполагается, что файл содержит список словарей

    # Фильтрация транзакций
    filtered = filter_transactions_by_description(transactions, 'перевод')
    print(filtered)

if __name__ == "__main__":
    with open('data/operations.json', 'r') as file:
        data = file.read()
    filtered = filter_transactions_by_description(data, 'перевод')