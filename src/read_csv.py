import csv
from datetime import datetime


def read_csv_file(file_path: str) -> list[dict]:
    result = []
    with open(file_path, "r", encoding="utf-8") as file:
        csvreader = csv.DictReader(file, delimiter=";")
        for row in csvreader:
            try:
                # Пробуем преобразовать id в int, если пусто — пропускаем или ставим None
                transaction_id = int(row["id"]) if row["id"].strip() else None

                formatted_row = {
                    "id": transaction_id,
                    "state": row["state"],
                    "date": row["date"],
                    "operationAmount": {
                        "amount": float(row["amount"]) if row["amount"].strip() else 0.0,
                        "currency": {"name": row["currency_name"], "code": row["currency_code"]},
                    },
                    "description": row["description"],
                    "from": row.get("from", ""),  # Используем get() для избежания KeyError
                    "to": row.get("to", ""),
                }
                result.append(formatted_row)
            except (ValueError, KeyError) as e:
                print(f"Ошибка в строке {row}: {e}")
    return result



