from src.processing import filter_by_state
from src.processing import sort_by_date
from src.utils import read_json
from src.read_csv import read_csv_file
from src.read_xlsx import read_xlsx_file
from src.filter_transactions import filter_transactions_by_description
from src.filter_rub_transactions import filter_rub_transactions
from datetime import datetime

def format_date(date_string):
    try:
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date_obj.strftime("%d.%m.%Y")
    except (ValueError, AttributeError):
        return date_string


def main_menu() -> list:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    file_selection = input()

    if file_selection == "1":
        print("Для обработки выбран JSON-файл.")
        transactions = read_json(r"C:\Users\LM\PycharmProjects\PythonProject1\data\operations.json")
    elif file_selection == "2":
        print("Для обработки выбран CSV-файл.")
        transactions = read_csv_file(r"C:\Users\LM\PycharmProjects\PythonProject1\data\transactions.csv")
    elif file_selection == "3":
        print("Для обработки выбран XLSX-файл.")
        transactions = read_xlsx_file(r"C:\Users\LM\PycharmProjects\PythonProject1\data\transactions_excel.xlsx")
    else:
        print("Введите корректный ответ.")
        return []

    ans1 = "executed"
    ans2 = "cancelled"
    ans3 = "pending"
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию. Доступные для фильтровки статусы: EXECUTED, CANCELLED, PENDING"
        )
        status = input().lower()
        if status in (ans1, ans2, ans3):
            print(f"Операции отфильтрованы по статусу {status}")
            filtered = filter_by_state(transactions, status)
            break
        else:
            print(f"Статус операции {status} недоступен.")

    sorting_date = filtered
    print("Отсортировать операции по дате? Да/Нет")
    date = input().lower()
    if date == "да":
        print("Отсортировать по возрастанию или по убыванию?")
        sorting = input().lower()
        if sorting == "по возрастанию":
            sorting_date = sort_by_date(filtered, flow=False)
        elif sorting == "по убыванию":
            sorting_date = sort_by_date(filtered, flow=True)

    current_transactions = sorting_date
    print("Выводить только рублевые транзакции? Да/Нет")
    choice_rub = input().lower()
    if choice_rub == "да":
        current_transactions = filter_rub_transactions(sorting_date)

    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    choice_word = input().lower()
    if choice_word == "да":
        search = input("Введите слово: ")
        current_transactions = filter_transactions_by_description(current_transactions, search)

    print("\nРаспечатываю итоговый список транзакций...")
    for i, tr in enumerate(current_transactions, 1):
        amount = tr.get('amount') or tr.get('operationAmount', {}).get('amount')

        currency = tr.get('currency')
        if isinstance(currency, dict):
            currency = currency.get('code') or currency.get('name')
        elif currency is None:
            currency = tr.get('operationAmount', {}).get('currency', '')
            if isinstance(currency, dict):
                currency = currency.get('code') or currency.get('name')

        description = tr.get('description', 'Без описания')

        date = format_date(tr.get('date', ''))

        print(f"{i}. {date} {description} - {amount or 'N/A'} {currency or ''}")

    return current_transactions


if __name__ == "__main__":
    main_menu()
