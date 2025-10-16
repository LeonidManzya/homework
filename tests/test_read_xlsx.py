from src.read_xlsx import read_xlsx_file
import pytest
import pandas as pd
import numpy as np
import os
from tempfile import NamedTemporaryFile



class TestReadXLSXFile:
    """Тесты для функции read_xlsx_file"""

    def create_test_xlsx(self, data: list[dict], columns: list = None) -> str:
        with NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            df = pd.DataFrame(data, columns=columns)
            df.to_excel(f.name, index=False, engine='openpyxl')
            return f.name

    def is_nan_value(self, value):
        if value is None:
            return True
        try:
            return pd.isna(value) or (isinstance(value, float) and np.isnan(value))
        except (TypeError, ValueError):
            return False

    def test_basic_functionality(self):
        test_data = [
            {"id": "1", "name": "Alice", "age": "25", "city": "New York"},
            {"id": "2", "name": "Bob", "age": "30", "city": "London"},
            {"id": "3", "name": "Charlie", "age": "35", "city": "Tokyo"}
        ]

        file_path = self.create_test_xlsx(test_data)
        try:
            result = read_xlsx_file(file_path)

            assert len(result) == 3
            # Сравниваем только не-NaN значения
            for i, expected_row in enumerate(test_data):
                for key, expected_value in expected_row.items():
                    assert result[i][key] == expected_value

        finally:
            os.unlink(file_path)

    def test_empty_file(self):
        file_path = self.create_test_xlsx([])
        try:
            result = read_xlsx_file(file_path)
            assert result == []
        finally:
            os.unlink(file_path)

    def test_empty_cells(self):
        test_data = [
            {"id": "1", "name": "Alice", "age": "", "city": "New York"},
            {"id": "2", "name": "", "age": "30", "city": ""},
            {"id": "", "name": "Charlie", "age": "35", "city": "Tokyo"}
        ]

        file_path = self.create_test_xlsx(test_data)
        try:
            result = read_xlsx_file(file_path)

            assert len(result) == 3

            assert result[0]["id"] == "1"
            assert result[0]["name"] == "Alice"
            assert self.is_nan_value(result[0]["age"])  # Пустая ячейка → NaN
            assert result[0]["city"] == "New York"

            assert result[1]["id"] == "2"
            assert self.is_nan_value(result[1]["name"])  # Пустая ячейка → NaN
            assert result[1]["age"] == "30"
            assert self.is_nan_value(result[1]["city"])  # Пустая ячейка → NaN

            assert self.is_nan_value(result[2]["id"])  # Пустая ячейка → NaN
            assert result[2]["name"] == "Charlie"
            assert result[2]["age"] == "35"
            assert result[2]["city"] == "Tokyo"

        finally:
            os.unlink(file_path)

    def test_none_values(self):
        data = {
            'col1': ['val1', None, 'val3'],
            'col2': [None, 'val2', None],
            'col3': ['val1', 'val2', np.nan]
        }
        df = pd.DataFrame(data)

        with NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            df.to_excel(f.name, index=False, engine='openpyxl')
            file_path = f.name

        try:
            result = read_xlsx_file(file_path)

            assert len(result) == 3

            # Проверяем NaN значения
            assert result[0]["col1"] == "val1"
            assert self.is_nan_value(result[0]["col2"])  # None → NaN
            assert result[0]["col3"] == "val1"

            assert self.is_nan_value(result[1]["col1"])  # None → NaN
            assert result[1]["col2"] == "val2"
            assert result[1]["col3"] == "val2"

            assert result[2]["col1"] == "val3"
            assert self.is_nan_value(result[2]["col2"])  # None → NaN
            assert self.is_nan_value(result[2]["col3"])  # NaN → NaN

        finally:
            os.unlink(file_path)

    def test_special_characters_and_unicode(self):
        """Тест специальных символов и Unicode"""
        test_data = [
            {
                "russian": "Привет мир",
                "chinese": "你好世界",
                "emoji": "😀🎉🌟",
                "special_chars": "a&b<c>d\"e'f@g#h$i%j^k(l)m-n=o+p",
                "html": "<div>test</div>",
                "whitespace": "  text with spaces  ",
            }
        ]

        file_path = self.create_test_xlsx(test_data)
        try:
            result = read_xlsx_file(file_path)

            assert len(result) == 1
            assert result[0]["russian"] == "Привет мир"
            assert result[0]["chinese"] == "你好世界"
            assert result[0]["emoji"] == "😀🎉🌟"
            assert result[0]["whitespace"] == "  text with spaces  "

        finally:
            os.unlink(file_path)

    def test_numeric_columns_as_strings(self):
        """Тест числовых колонок, которые читаются как строки"""
        test_data = [
            {"numeric_id": "001", "price": "19.99", "quantity": "100"},
            {"numeric_id": "002", "price": "0.99", "quantity": "050"},
            {"numeric_id": "003", "price": "999.00", "quantity": "001"}
        ]

        file_path = self.create_test_xlsx(test_data)
        try:
            result = read_xlsx_file(file_path)

            assert len(result) == 3
            # Все значения должны быть строками, включая ведущие нули
            assert result[0]["numeric_id"] == "001"
            assert result[1]["quantity"] == "050"
            assert result[2]["quantity"] == "001"

        finally:
            os.unlink(file_path)

    def test_file_not_found(self):
        """Тест случая когда файл не существует"""
        with pytest.raises(FileNotFoundError) as exc_info:
            read_xlsx_file("nonexistent_file.xlsx")

        assert "Файл не найден: nonexistent_file.xlsx" in str(exc_info.value)

    @pytest.mark.parametrize("test_data,expected_count", [
        ([{"id": "1"}], 1),
        ([{"a": "1"}, {"a": "2"}, {"a": "3"}], 3),
        ([], 0),
    ])
    def test_parametrized_data(self, test_data, expected_count):
        """Параметризованный тест различных наборов данных"""
        file_path = self.create_test_xlsx(test_data)
        try:
            result = read_xlsx_file(file_path)
            assert len(result) == expected_count
        finally:
            os.unlink(file_path)

    def test_mixed_data_types_preserved_as_strings(self):
        """Тест что разные типы данных сохраняются как строки"""
        test_data = [
            {
                "integer": "123",
                "float": "45.67",
                "boolean": "True",
                "text": "hello",
                "zero": "0",
                "negative": "-5.5"
            }
        ]

        file_path = self.create_test_xlsx(test_data)
        try:
            result = read_xlsx_file(file_path)

            assert len(result) == 1
            assert result[0]["integer"] == "123"
            assert result[0]["float"] == "45.67"
            assert result[0]["boolean"] == "True"
            assert result[0]["zero"] == "0"
            assert result[0]["negative"] == "-5.5"

        finally:
            os.unlink(file_path)

    def test_complex_structure(self):
        """Тест сложной структуры данных"""
        test_data = [
            {
                "id": "1", "name": "Test User", "email": "test@example.com",
                "address": "123 Main St", "phone": "+1-555-0123",
                "notes": "Regular customer", "status": "active"
            },
            {
                "id": "2", "name": "Another User", "email": "another@example.com",
                "address": "", "phone": "", "notes": "", "status": "pending"
            }
        ]

        file_path = self.create_test_xlsx(test_data)
        try:
            result = read_xlsx_file(file_path)

            assert len(result) == 2

            assert result[0]["id"] == "1"
            assert result[0]["name"] == "Test User"
            assert result[0]["email"] == "test@example.com"

            assert result[1]["id"] == "2"
            assert result[1]["name"] == "Another User"
            assert result[1]["email"] == "another@example.com"
            assert self.is_nan_value(result[1]["address"])
            assert self.is_nan_value(result[1]["phone"])
            assert self.is_nan_value(result[1]["notes"])
            assert result[1]["status"] == "pending"

        finally:
            os.unlink(file_path)