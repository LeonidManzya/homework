import csv

def read_csv_file(file_path: str) -> list[dict]:

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter= ';')
            for row in reader:
                print(row['id'], row["state"], row["date"], row["amount"], row["currency_name"], row["currency_code"],
                      row["from"], row["to"], row["description"])
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {file_path}")

print(read_csv_file(r"..\\data\\transactions.csv"))