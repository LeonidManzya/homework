import unittest
from unittest.mock import patch

from src.utils import read_json


class TestTransactions(unittest.TestCase):
    @patch("builtins.open")
    @patch("json.load")
    def test_read_correct_json(self, mock_json_load, mock_open_file):
        """Тест чтения корректного JSON-файла"""

        mock_json_load.return_value = [{"key": "value"}]
        result = read_json("test.json")

        self.assertEqual(result, [{"key": "value"}])

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_file_not_found(self, mock_open):
        """Тест чтения отсутствующего файла"""

        with self.assertRaises(FileNotFoundError):
            read_json("path/to/nonexistent/file.json")

        # Проверяем, что функция open была вызвана с правильными аргументами
        mock_open.assert_called_once_with("path/to/nonexistent/file.json", "r", encoding="utf-8")

    @patch("builtins.open")
    @patch("json.load")
    def test_read_invalid_json_structure(self, mock_json_load, mock_open_file):
        """Тест чтения некорректного JSON-файла"""

        mock_json_load.return_value = {"key": "value"}

        with self.assertRaises(ValueError) as context:
            read_json("invalid.json")

        self.assertEqual(str(context.exception), "JSON файл должен содержать список")
        mock_open_file.assert_called_once_with("invalid.json", "r", encoding="utf-8")