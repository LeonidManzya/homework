import csv

def read_csv_file(file_path: str) -> list[dict]:

    try:
        dikct_list = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter= ';')
            for row in reader:
                dict = {"id": row['id'], "state": row["state"], "date": row["date"],
                       "amount": row["amount"], "currency_name": row["currency_name"],
                       "currency_code": row["currency_code"], "from": row["from"], "to": row["to"],
                       "description": row["description"]}
                dikct_list.append(dict)
        return dikct_list
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")

print(read_csv_file(r"..\\data\\transactions.csv"))