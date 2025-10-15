import json
from collections import Counter
from typing import List, Dict, Any


def count_operations_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:

    category_counts = Counter({category: 0 for category in categories})
    lower_categories = {cat.lower(): cat for cat in categories}

    for transaction in transactions:
        description = transaction.get("description", "").lower()
        for lower_cat, original_cat in lower_categories.items():
            if lower_cat in description:
                category_counts[original_cat] += 1
                break

    return dict(category_counts)


if __name__ == "__main__":
    try:

        with open(r"C:\Users\LM\PycharmProjects\PythonProject1\data\operations.json", "r", encoding="utf-8") as file:
            transactions = json.load(file)

        categories = ["открытие", "пополнение", "перевод"]

        operations_count = count_operations_by_category(transactions, categories)
        print("Количество операций по категориям:")
        for category, count in operations_count.items():
            print(f"{category}: {count}")

    except FileNotFoundError:
        print("Ошибка: файл не найден!")
    except json.JSONDecodeError:
        print("Ошибка: файл содержит некорректный JSON!")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
