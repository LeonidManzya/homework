from src.filter_transactions import filter_transactions_by_description
import pytest


class TestFilterTransactionsByDescription:
    """Тесты для функции filter_transactions_by_description"""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с примерными транзакциями"""
        return [
            {"id": 1, "description": "Payment for groceries", "amount": 100},
            {"id": 2, "description": "Transfer to John", "amount": 200},
            {"id": 3, "description": "Online purchase AMAZON", "amount": 50},
            {"id": 4, "description": "Restaurant payment", "amount": 75},
            {"id": 5, "description": "AMAZON prime subscription", "amount": 10},
            {"id": 6, "description": "", "amount": 30},  # пустое описание
            {"id": 7, "description": "UPPERCASE PAYMENT", "amount": 40},
            {"id": 8, "description": "lowercase transfer", "amount": 60},
            {"id": 9, "description": "Mixed Case Payment", "amount": 80},
        ]

    def test_basic_filtering(self, sample_transactions):
        """Тест базовой фильтрации"""
        result = filter_transactions_by_description(sample_transactions, "amazon")
        assert len(result) == 2
        assert result[0]["id"] == 3
        assert result[1]["id"] == 5

    def test_case_insensitivity(self, sample_transactions):
        """Тест регистронезависимого поиска"""
        result_upper = filter_transactions_by_description(sample_transactions, "PAYMENT")
        result_lower = filter_transactions_by_description(sample_transactions, "payment")
        result_mixed = filter_transactions_by_description(sample_transactions, "Payment")

        # Все варианты должны вернуть одинаковый результат
        expected_ids = {1, 4, 7, 9}
        assert {t["id"] for t in result_upper} == expected_ids
        assert {t["id"] for t in result_lower} == expected_ids
        assert {t["id"] for t in result_mixed} == expected_ids

    def test_no_matches(self, sample_transactions):
        """Тест случая, когда нет совпадений"""
        result = filter_transactions_by_description(sample_transactions, "nonexistent")
        assert result == []

    def test_empty_transactions_list(self):
        """Тест с пустым списком транзакций"""
        result = filter_transactions_by_description([], "test")
        assert result == []

    def test_empty_search_pattern(self, sample_transactions):
        """Тест с пустой строкой поиска"""
        result = filter_transactions_by_description(sample_transactions, "")
        # Пустой паттерн должен вернуть все транзакции
        assert len(result) == len(sample_transactions)

    def test_special_characters_in_pattern(self, sample_transactions):
        """Тест с специальными символами в паттерне"""
        # Добавим транзакцию со специальными символами
        transactions_with_special = sample_transactions + [
            {"id": 10, "description": "Payment (urgent!)", "amount": 90}
        ]

        # Специальные символы должны быть экранированы
        result = filter_transactions_by_description(transactions_with_special, "(urgent!)")
        assert len(result) == 1
        assert result[0]["id"] == 10


    def test_partial_matches(self, sample_transactions):
        """Тест частичных совпадений"""
        result = filter_transactions_by_description(sample_transactions, "pay")
        expected_ids = {1, 4, 7, 9}  # Все транзакции с "payment" в описании
        assert {t["id"] for t in result} == expected_ids

    def test_multiple_words_pattern(self, sample_transactions):
        """Тест поиска по нескольким словам"""
        result = filter_transactions_by_description(sample_transactions, "online purchase")
        assert len(result) == 1
        assert result[0]["id"] == 3

    @pytest.mark.parametrize("pattern,expected_count", [
        ("amazon", 2),
        ("payment", 4),
        ("transfer", 2),
        ("restaurant", 1),
        ("subscription", 1),
        ("nonexistent", 0),
    ])
    def test_parametrized_search(self, sample_transactions, pattern, expected_count):
        """Параметризованный тест различных паттернов поиска"""
        result = filter_transactions_by_description(sample_transactions, pattern)
        assert len(result) == expected_count

    def test_invalid_regex_pattern(self, sample_transactions):
        """Тест с некорректным regex паттерном"""
        # Функция экранирует спецсимволы, поэтому даже некорректные паттерны
        # должны обрабатываться корректно
        result = filter_transactions_by_description(sample_transactions, "[invalid")
        assert result == []  # Согласно реализации, при ошибке regex возвращается пустой список

    def test_whitespace_handling(self):
        """Тест обработки пробелов"""
        transactions = [
            {"id": 1, "description": "  Payment with spaces  ", "amount": 100},
            {"id": 2, "description": "Payment\nwith\nnewlines", "amount": 200},
            {"id": 3, "description": "Payment\twith\ttabs", "amount": 300},
        ]

        result = filter_transactions_by_description(transactions, "payment")
        assert len(result) == 3

    def test_unicode_characters(self):
        """Тест с Unicode символами"""
        transactions = [
            {"id": 1, "description": "Payment café", "amount": 100},
            {"id": 2, "description": "Transfer für", "amount": 200},
            {"id": 3, "description": "Платеж магазин", "amount": 300},
        ]

        result = filter_transactions_by_description(transactions, "café")
        assert len(result) == 1
        assert result[0]["id"] == 1

        result = filter_transactions_by_description(transactions, "Платеж")
        assert len(result) == 1
        assert result[0]["id"] == 3