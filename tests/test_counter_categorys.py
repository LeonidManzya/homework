from src.counter_categorys import count_operations_by_category
import pytest



class TestCountOperationsByCategory:
    """Тесты для функции count_operations_by_category"""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с примерными транзакциями"""
        return [
            {"id": 1, "description": "Открытие вклада", "amount": 1000},
            {"id": 2, "description": "Пополнение счета", "amount": 500},
            {"id": 3, "description": "Перевод другу", "amount": 200},
            {"id": 4, "description": "Открытие карты", "amount": 0},
            {"id": 5, "description": "пополнение телефона", "amount": 100},
            {"id": 6, "description": "ПЕРЕВОД В БАНК", "amount": 300},
            {"id": 7, "description": "ОТКРЫтие депозита", "amount": 1500},
            {"id": 8, "description": "Оплата услуг", "amount": 50},
            {"id": 9, "description": "Перевод на карту", "amount": 250},
            {"id": 10, "description": "пополнение с карты", "amount": 400},
        ]

    def test_basic_functionality(self, sample_transactions):
        """Тест базовой функциональности"""
        categories = ["открытие", "пополнение", "перевод"]
        result = count_operations_by_category(sample_transactions, categories)

        expected = {
            "открытие": 3,
            "пополнение": 3,
            "перевод": 3
        }
        assert result == expected

    def test_case_insensitivity(self, sample_transactions):
        """Тест регистронезависимости"""
        categories = ["открытие", "пополнение", "перевод"]
        result = count_operations_by_category(sample_transactions, categories)

        assert result["открытие"] == 3
        assert result["пополнение"] == 3
        assert result["перевод"] == 3

    def test_no_matches(self, sample_transactions):
        """Тест когда нет совпадений"""
        categories = ["кредит", "страхование", "инвестиции"]
        result = count_operations_by_category(sample_transactions, categories)

        expected = {"кредит": 0, "страхование": 0, "инвестиции": 0}
        assert result == expected

    def test_empty_transactions_list(self):
        """Тест с пустым списком транзакций"""
        categories = ["открытие", "пополнение"]
        result = count_operations_by_category([], categories)

        expected = {"открытие": 0, "пополнение": 0}
        assert result == expected

    def test_empty_categories_list(self, sample_transactions):
        """Тест с пустым списком категорий"""
        result = count_operations_by_category(sample_transactions, [])
        assert result == {}


    def test_order_of_categories_matters(self):
        """Тест что порядок категорий важен - учитывается первая найденная"""
        transactions = [
            {"id": 1, "description": "перевод и открытие", "amount": 100},
        ]

        categories1 = ["перевод", "открытие"]
        result1 = count_operations_by_category(transactions, categories1)
        assert result1 == {"перевод": 1, "открытие": 0}

        categories2 = ["открытие", "перевод"]
        result2 = count_operations_by_category(transactions, categories2)
        assert result2 == {"открытие": 1, "перевод": 0}

    def test_special_characters_in_categories(self):
        """Тест специальных символов в категориях"""
        transactions = [
            {"id": 1, "description": "оплата (срочная)", "amount": 100},
            {"id": 2, "description": "перевод-онлайн", "amount": 200},
        ]
        categories = ["оплата (срочная)", "перевод-онлайн"]
        result = count_operations_by_category(transactions, categories)

        expected = {"оплата (срочная)": 1, "перевод-онлайн": 1}
        assert result == expected

    @pytest.mark.parametrize("categories,expected", [
        (["открытие"], {"открытие": 3}),
        (["пополнение"], {"пополнение": 3}),
        (["перевод"], {"перевод": 3}),
        (["открытие", "пополнение"], {"открытие": 3, "пополнение": 3}),
    ])
    def test_parametrized_categories(self, sample_transactions, categories, expected):
        """Параметризованный тест различных наборов категорий"""
        result = count_operations_by_category(sample_transactions, categories)
        assert result == expected

    def test_duplicate_categories(self):
        """Тест с дублирующимися категориями"""
        transactions = [
            {"id": 1, "description": "открытие счета", "amount": 100},
        ]
        categories = ["открытие", "открытие", "пополнение"]
        result = count_operations_by_category(transactions, categories)

        expected = {"открытие": 1, "пополнение": 0}
        assert result == expected

    def test_unicode_and_cyrillic(self):
        """Тест с Unicode и кириллическими символами"""
        transactions = [
            {"id": 1, "description": "Öffnung Konto", "amount": 100},
            {"id": 2, "description": "Пополнение счёта", "amount": 200},
            {"id": 3, "description": "開戶", "amount": 300},
        ]
        categories = ["öffnung", "пополнение", "開戶"]
        result = count_operations_by_category(transactions, categories)

        expected = {"öffnung": 1, "пополнение": 1, "開戶": 1}
        assert result == expected