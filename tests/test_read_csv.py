from src.read_csv import read_csv_file
import pytest
import csv
import os
from tempfile import NamedTemporaryFile


class TestReadCSVFile:

    def create_test_csv(self, content: list, fieldnames: list = None) -> str:
        """Создает временный CSV файл для тестирования"""
        if fieldnames is None:
            fieldnames = ["id", "state", "date", "amount", "currency_name",
                          "currency_code", "description", "from", "to"]

        with NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for row in content:
                writer.writerow(row)
            return f.name

    def test_basic_functionality(self):
        """Тест базовой функциональности"""
        test_data = [
            {
                "id": "1", "state": "EXECUTED", "date": "2023-10-01T12:00:00",
                "amount": "100.50", "currency_name": "US Dollar", "currency_code": "USD",
                "description": "Payment", "from": "Visa 1234", "to": "Account 5678"
            },
            {
                "id": "2", "state": "CANCELED", "date": "2023-10-02T14:30:00",
                "amount": "200.75", "currency_name": "Euro", "currency_code": "EUR",
                "description": "Transfer", "from": "MasterCard 4321", "to": "Account 8765"
            }
        ]

        file_path = self.create_test_csv(test_data)
        try:
            result = read_csv_file(file_path)

            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[0]["state"] == "EXECUTED"
            assert result[0]["date"] == "2023-10-01T12:00:00"
            assert result[0]["operationAmount"]["amount"] == 100.50
            assert result[0]["operationAmount"]["currency"]["name"] == "US Dollar"
            assert result[0]["operationAmount"]["currency"]["code"] == "USD"
            assert result[0]["description"] == "Payment"
            assert result[0]["from"] == "Visa 1234"
            assert result[0]["to"] == "Account 5678"
            assert result[1]["id"] == 2
            assert result[1]["state"] == "CANCELED"

        finally:
            os.unlink(file_path)

    def test_empty_values(self):
        """Тест обработки пустых значений"""
        test_data = [
            {
                "id": "", "state": "PENDING", "date": "2023-10-03T10:00:00",
                "amount": "", "currency_name": "Ruble", "currency_code": "RUB",
                "description": "Empty values", "from": "", "to": ""
            }
        ]

        file_path = self.create_test_csv(test_data)
        try:
            result = read_csv_file(file_path)

            assert len(result) == 1
            assert result[0]["id"] is None
            assert result[0]["operationAmount"]["amount"] == 0.0
            assert result[0]["from"] == ""
            assert result[0]["to"] == ""

        finally:
            os.unlink(file_path)

    def test_whitespace_values(self):
        """Тест обработки значений с пробелами"""
        test_data = [
            {
                "id": "  3  ", "state": "  EXECUTED  ", "date": "  2023-10-04T09:00:00  ",
                "amount": "  150.25  ", "currency_name": "  Yen  ", "currency_code": "  JPY  ",
                "description": "  With spaces  ", "from": "  Card 9999  ", "to": "  Account 1111  "
            }
        ]

        file_path = self.create_test_csv(test_data)
        try:
            result = read_csv_file(file_path)

            assert len(result) == 1
            assert result[0]["id"] == 3
            assert result[0]["state"] == "  EXECUTED  "
            assert result[0]["operationAmount"]["amount"] == 150.25
            assert result[0]["operationAmount"]["currency"]["name"] == "  Yen  "

        finally:
            os.unlink(file_path)

    def test_invalid_id_format(self):
        """Тест некорректного формата id"""
        test_data = [
            {
                "id": "invalid", "state": "EXECUTED", "date": "2023-10-05T08:00:00",
                "amount": "100.0", "currency_name": "Dollar", "currency_code": "USD",
                "description": "Invalid ID", "from": "Card 123", "to": "Account 456"
            }
        ]

        file_path = self.create_test_csv(test_data)
        try:
            result = read_csv_file(file_path)
            assert len(result) == 0

        finally:
            os.unlink(file_path)

    def test_invalid_amount_format(self):
        """Тест некорректного формата amount"""
        test_data = [
            {
                "id": "4", "state": "EXECUTED", "date": "2023-10-06T07:00:00",
                "amount": "not_a_number", "currency_name": "Euro", "currency_code": "EUR",
                "description": "Invalid amount", "from": "Card 777", "to": "Account 888"
            }
        ]

        file_path = self.create_test_csv(test_data)
        try:
            result = read_csv_file(file_path)
            assert len(result) == 0

        finally:
            os.unlink(file_path)

    def test_missing_required_fields(self):
        """Тест отсутствия обязательных полей"""
        test_data = [
            {
                "id": "5", "state": "EXECUTED",
            }
        ]

        file_path = self.create_test_csv(test_data, fieldnames=["id", "state"])
        try:
            result = read_csv_file(file_path)
            assert len(result) == 0

        finally:
            os.unlink(file_path)

    def test_optional_fields_missing(self):
        """Тест отсутствия опциональных полей 'from' и 'to'"""
        test_data = [
            {
                "id": "6", "state": "EXECUTED", "date": "2023-10-07T06:00:00",
                "amount": "300.0", "currency_name": "Pound", "currency_code": "GBP",
                "description": "No from/to"
            }
        ]

        file_path = self.create_test_csv(test_data,
                                         fieldnames=["id", "state", "date", "amount",
                                                     "currency_name", "currency_code", "description"])
        try:
            result = read_csv_file(file_path)

            assert len(result) == 1
            assert result[0]["from"] == ""
            assert result[0]["to"] == ""

        finally:
            os.unlink(file_path)

    def test_different_numeric_formats(self):
        """Тест различных числовых форматов"""
        test_data = [
            {
                "id": "7", "state": "EXECUTED", "date": "2023-10-08T05:00:00",
                "amount": "1000", "currency_name": "Dollar", "currency_code": "USD",
                "description": "Integer amount", "from": "Card 111", "to": "Account 222"
            },
            {
                "id": "8", "state": "EXECUTED", "date": "2023-10-09T04:00:00",
                "amount": "999.99", "currency_name": "Euro", "currency_code": "EUR",
                "description": "Decimal amount", "from": "Card 333", "to": "Account 444"
            },
            {
                "id": "9", "state": "EXECUTED", "date": "2023-10-10T03:00:00",
                "amount": "0", "currency_name": "Yen", "currency_code": "JPY",
                "description": "Zero amount", "from": "Card 555", "to": "Account 666"
            }
        ]

        file_path = self.create_test_csv(test_data)
        try:
            result = read_csv_file(file_path)

            assert len(result) == 3
            assert result[0]["operationAmount"]["amount"] == 1000.0
            assert result[1]["operationAmount"]["amount"] == 999.99
            assert result[2]["operationAmount"]["amount"] == 0.0

        finally:
            os.unlink(file_path)

    def test_special_characters(self):
        """Тест специальных символов и Unicode"""
        test_data = [
            {
                "id": "10", "state": "EXECUTED", "date": "2023-10-11T02:00:00",
                "amount": "150.75", "currency_name": "Рубль", "currency_code": "RUB",
                "description": "Платеж за кафе", "from": "Карта 1234", "to": "Счёт 5678"
            },
            {
                "id": "11", "state": "EXECUTED", "date": "2023-10-12T01:00:00",
                "amount": "200.50", "currency_name": "€", "currency_code": "EUR",
                "description": "Payment & Transfer > Online", "from": "Card (Visa)", "to": "Account #123"
            }
        ]

        file_path = self.create_test_csv(test_data)
        try:
            result = read_csv_file(file_path)

            assert len(result) == 2
            assert result[0]["description"] == "Платеж за кафе"
            assert result[0]["operationAmount"]["currency"]["name"] == "Рубль"
            assert result[1]["description"] == "Payment & Transfer > Online"

        finally:
            os.unlink(file_path)

    def test_empty_file(self):
        """Тест пустого файла (только заголовок)"""
        file_path = self.create_test_csv([])
        try:
            result = read_csv_file(file_path)
            assert result == []
        finally:
            os.unlink(file_path)

    def test_large_numbers(self):
        """Тест больших чисел"""
        test_data = [
            {
                "id": "1234567890", "state": "EXECUTED", "date": "2023-10-13T00:00:00",
                "amount": "999999999.99", "currency_name": "Dollar", "currency_code": "USD",
                "description": "Large numbers", "from": "Card 999", "to": "Account 000"
            }
        ]

        file_path = self.create_test_csv(test_data)
        try:
            result = read_csv_file(file_path)

            assert len(result) == 1
            assert result[0]["id"] == 1234567890
            assert result[0]["operationAmount"]["amount"] == 999999999.99

        finally:
            os.unlink(file_path)

    def test_file_not_found(self):
        """Тест случая когда файл не существует"""
        with pytest.raises(FileNotFoundError):
            read_csv_file("nonexistent_file.csv")