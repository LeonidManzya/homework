import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from src.main import main_menu


class TestMainMenu:
    """Тесты для функции main_menu"""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с примерными транзакциями"""
        return [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-10-01T12:00:00",
                "operationAmount": {
                    "amount": 100.50,
                    "currency": {"name": "US Dollar", "code": "USD"}
                },
                "description": "Payment for services",
                "from": "Visa 1234",
                "to": "Account 5678"
            },
            {
                "id": 2,
                "state": "CANCELED",
                "date": "2023-10-02T14:30:00",
                "operationAmount": {
                    "amount": 200.75,
                    "currency": {"name": "Ruble", "code": "RUB"}
                },
                "description": "Transfer to friend",
                "from": "MasterCard 4321",
                "to": "Account 8765"
            }
        ]

    @pytest.fixture
    def mock_functions(self):
        """Фикстура для мокинга всех внешних функций"""
        with patch('src.main.read_json') as mock_read_json, \
                patch('src.main.read_csv_file') as mock_read_csv, \
                patch('src.main.read_xlsx_file') as mock_read_xlsx, \
                patch('src.main.filter_by_state') as mock_filter_state, \
                patch('src.main.sort_by_date') as mock_sort_date, \
                patch('src.main.filter_rub_transactions') as mock_filter_rub, \
                patch('src.main.filter_transactions_by_description') as mock_filter_desc:
            mocks = {
                'read_json': mock_read_json,
                'read_csv': mock_read_csv,
                'read_xlsx': mock_read_xlsx,
                'filter_state': mock_filter_state,
                'sort_date': mock_sort_date,
                'filter_rub': mock_filter_rub,
                'filter_desc': mock_filter_desc
            }

            # Настраиваем возвращаемые значения по умолчанию
            mock_read_json.return_value = []
            mock_read_csv.return_value = []
            mock_read_xlsx.return_value = []
            mock_filter_state.return_value = []
            mock_sort_date.return_value = []
            mock_filter_rub.return_value = []
            mock_filter_desc.return_value = []

            yield mocks

    def capture_output(self, func, *args, **kwargs):
        """Вспомогательная функция для захвата вывода"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        try:
            result = func(*args, **kwargs)
            output = captured_output.getvalue()
            return result, output
        finally:
            sys.stdout = old_stdout

    def test_invalid_file_selection(self, mock_functions):
        """Тест некорректного выбора файла"""
        user_input = [
            "4",  # неверный выбор файла
        ]

        with patch('builtins.input', side_effect=user_input):
            result, output = self.capture_output(main_menu)

            assert result == []
            assert "Введите корректный ответ" in output

    def test_json_file_selection(self, mock_functions, sample_transactions):
        """Тест выбора JSON файла"""
        mock_functions['read_json'].return_value = sample_transactions

        user_input = [
            "1",  # JSON файл
            "executed",  # статус
            "нет",  # сортировка по дате
            "нет",  # рублевые транзакции
            "нет"  # фильтрация по описанию
        ]

        with patch('builtins.input', side_effect=user_input):
            result, output = self.capture_output(main_menu)

            mock_functions['read_json'].assert_called_once()
            assert "Для обработки выбран JSON-файл" in output

    def test_csv_file_selection(self, mock_functions, sample_transactions):
        """Тест выбора CSV файла"""
        mock_functions['read_csv'].return_value = sample_transactions

        user_input = [
            "2",  # CSV файл
            "executed",  # статус
            "нет",  # сортировка по дате
            "нет",  # рублевые транзакции
            "нет"  # фильтрация по описанию
        ]

        with patch('builtins.input', side_effect=user_input):
            result, output = self.capture_output(main_menu)

            mock_functions['read_csv'].assert_called_once()
            assert "Для обработки выбран CSV-файл" in output

    def test_xlsx_file_selection(self, mock_functions, sample_transactions):
        """Тест выбора XLSX файла"""
        mock_functions['read_xlsx'].return_value = sample_transactions

        user_input = [
            "3",  # XLSX файл
            "executed",  # статус
            "нет",  # сортировка по дате
            "нет",  # рублевые транзакции
            "нет"  # фильтрация по описанию
        ]

        with patch('builtins.input', side_effect=user_input):
            result, output = self.capture_output(main_menu)

            mock_functions['read_xlsx'].assert_called_once()
            assert "Для обработки выбран XLSX-файл" in output

    def test_status_filtering_valid_status(self, mock_functions, sample_transactions):
        """Тест фильтрации по валидному статусу"""
        mock_functions['read_json'].return_value = sample_transactions
        mock_functions['filter_state'].return_value = [sample_transactions[0]]  # только EXECUTED

        user_input = [
            "1",  # JSON файл
            "executed",  # статус
            "нет",  # сортировка по дате
            "нет",  # рублевые транзакции
            "нет"  # фильтрация по описанию
        ]

        with patch('builtins.input', side_effect=user_input):
            result = main_menu()

            mock_functions['filter_state'].assert_called_once_with(sample_transactions, "executed")

    def test_status_filtering_invalid_status(self, mock_functions, sample_transactions):
        """Тест фильтрации по невалидному статусу с последующим исправлением"""
        mock_functions['read_json'].return_value = sample_transactions

        user_input = [
            "1",  # JSON файл
            "invalid_status",  # неверный статус
            "executed",  # верный статус
            "нет",  # сортировка по дате
            "нет",  # рублевые транзакции
            "нет"  # фильтрация по описанию
        ]

        with patch('builtins.input', side_effect=user_input):
            result, output = self.capture_output(main_menu)

            assert "недоступен" in output
            mock_functions['filter_state'].assert_called_once_with(sample_transactions, "executed")

    def test_date_sorting_ascending(self, mock_functions, sample_transactions):
        """Тест сортировки по возрастанию"""
        filtered_transactions = [sample_transactions[0]]

        mock_functions['read_json'].return_value = sample_transactions
        mock_functions['filter_state'].return_value = filtered_transactions
        mock_functions['sort_date'].return_value = filtered_transactions

        user_input = [
            "1",  # JSON файл
            "executed",  # статус
            "да",  # сортировка по дате
            "по возрастанию",  # направление сортировки
            "нет",  # рублевые транзакции
            "нет"  # фильтрация по описанию
        ]

        with patch('builtins.input', side_effect=user_input):
            result = main_menu()

            mock_functions['sort_date'].assert_called_once_with(filtered_transactions, flow=False)

    def test_date_sorting_descending(self, mock_functions, sample_transactions):
        """Тест сортировки по убыванию"""
        filtered_transactions = [sample_transactions[0]]

        mock_functions['read_json'].return_value = sample_transactions
        mock_functions['filter_state'].return_value = filtered_transactions
        mock_functions['sort_date'].return_value = filtered_transactions

        user_input = [
            "1",  # JSON файл
            "executed",  # статус
            "да",  # сортировка по дате
            "по убыванию",  # направление сортировки
            "нет",  # рублевые транзакции
            "нет"  # фильтрация по описанию
        ]

        with patch('builtins.input', side_effect=user_input):
            result = main_menu()

            mock_functions['sort_date'].assert_called_once_with(filtered_transactions, flow=True)

    def test_rub_transactions_filter(self, mock_functions, sample_transactions):
        """Тест фильтрации рублевых транзакций"""
        filtered_transactions = [sample_transactions[0]]
        rub_transactions = [sample_transactions[1]]  # только RUB

        mock_functions['read_json'].return_value = sample_transactions
        mock_functions['filter_state'].return_value = filtered_transactions
        mock_functions['filter_rub'].return_value = rub_transactions

        user_input = [
            "1",  # JSON файл
            "executed",  # статус
            "нет",  # сортировка по дате
            "да",  # рублевые транзакции
            "нет"  # фильтрация по описанию
        ]

        with patch('builtins.input', side_effect=user_input):
            result = main_menu()

            mock_functions['filter_rub'].assert_called_once_with(filtered_transactions)

    def test_description_filter(self, mock_functions, sample_transactions):
        """Тест фильтрации по описанию"""
        filtered_transactions = [sample_transactions[0]]
        desc_filtered = [sample_transactions[0]]

        mock_functions['read_json'].return_value = sample_transactions
        mock_functions['filter_state'].return_value = filtered_transactions
        mock_functions['filter_desc'].return_value = desc_filtered

        user_input = [
            "1",  # JSON файл
            "executed",  # статус
            "нет",  # сортировка по дате
            "нет",  # рублевые транзакции
            "да",  # фильтрация по описанию
            "Payment"  # слово для поиска
        ]

        with patch('builtins.input', side_effect=user_input):
            result = main_menu()

            mock_functions['filter_desc'].assert_called_once_with(filtered_transactions, "Payment")

    def test_output_formatting(self, mock_functions):
        """Тест форматирования вывода"""
        test_transactions = [
            {
                "description": "Test payment",
                "amount": 100.0,
                "operationAmount": {"amount": 100.0, "currency": {"code": "USD"}}
            },
            {
                "description": "Another transaction",
                "operationAmount": {"amount": 200.0, "currency": {"name": "Ruble"}}
            },
            {
                "description": "No amount",
                "operationAmount": {"currency": {"code": "EUR"}}
            }
        ]

        mock_functions['read_json'].return_value = test_transactions
        mock_functions['filter_state'].return_value = test_transactions

        user_input = [
            "1",  # JSON файл
            "executed",  # статус
            "нет",  # сортировка по дате
            "нет",  # рублевые транзакции
            "нет"  # фильтрация по описанию
        ]

        with patch('builtins.input', side_effect=user_input):
            result, output = self.capture_output(main_menu)

            assert "Распечатываю итоговый список транзакций" in output
            assert "Test payment - 100.0 USD" in output
            assert "Another transaction - 200.0 Ruble" in output
            assert "No amount - N/A" in output

    def test_empty_transactions_after_filtering(self, mock_functions, sample_transactions):
        """Тест когда после фильтрации не осталось транзакций"""
        mock_functions['read_json'].return_value = sample_transactions
        mock_functions['filter_state'].return_value = []  # все отфильтровались
        mock_functions['filter_desc'].return_value = []  # фильтр по описанию тоже пустой

        user_input = [
            "1",  # JSON файл
            "executed",  # статус
            "нет",  # сортировка по дате
            "нет",  # рублевые транзакции
            "да",  # фильтрация по описанию
            "nonexistent"  # слово которого нет
        ]

        with patch('builtins.input', side_effect=user_input):
            result, output = self.capture_output(main_menu)

            assert result == []
            assert "Распечатываю итоговый список транзакций" in output

    def test_complete_workflow(self, mock_functions, sample_transactions):
        """Тест полного рабочего процесса"""
        filtered_by_state = [sample_transactions[0]]
        sorted_transactions = [sample_transactions[0]]
        rub_transactions = [sample_transactions[0]]
        final_transactions = [sample_transactions[0]]

        mock_functions['read_json'].return_value = sample_transactions
        mock_functions['filter_state'].return_value = filtered_by_state
        mock_functions['sort_date'].return_value = sorted_transactions
        mock_functions['filter_rub'].return_value = rub_transactions
        mock_functions['filter_desc'].return_value = final_transactions

        user_input = [
            "1",  # JSON файл
            "executed",  # статус
            "да",  # сортировка по дате
            "по возрастанию",  # направление сортировки
            "да",  # рублевые транзакции
            "да",  # фильтрация по описанию
            "Payment"  # слово для поиска
        ]

        with patch('builtins.input', side_effect=user_input):
            result = main_menu()

            # Проверяем что все функции были вызваны в правильном порядке
            mock_functions['read_json'].assert_called_once()
            mock_functions['filter_state'].assert_called_once()
            mock_functions['sort_date'].assert_called_once()
            mock_functions['filter_rub'].assert_called_once()
            mock_functions['filter_desc'].assert_called_once()

            assert result == final_transactions

    @pytest.mark.parametrize("file_choice,expected_function", [
        ("1", "read_json"),
        ("2", "read_csv"),
        ("3", "read_xlsx"),
    ])
    def test_parametrized_file_selection(self, mock_functions, file_choice, expected_function):
        """Параметризованный тест выбора файла"""
        user_input = [
            file_choice,
            "executed",
            "нет",
            "нет",
            "нет"
        ]

        with patch('builtins.input', side_effect=user_input):
            main_menu()

            mock_func = mock_functions[expected_function]
            mock_func.assert_called_once()