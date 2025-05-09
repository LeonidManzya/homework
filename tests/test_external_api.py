from unittest.mock import patch

from src.external_api import convert_transaction


@patch("src.external_api.requests.get")
def test_convert(mock_requests_get):
    """Тест для конвертации валюты в RUB"""

    mock_requests_get.return_value.json.return_value = {"result": 75.0}

    test_transaction = {"operationAmount": {"amount": "1.00", "currency": {"code": "USD"}}}
    assert convert_transaction(test_transaction) == 75.0


def test_rub_transaction():
    """Тест для RUB без конвертации"""

    test_transaction = {"operationAmount": {"amount": "1000.00", "currency": {"code": "RUB"}}}

    assert convert_transaction(test_transaction) == 1000.0


@patch("src.external_api.requests.get")
def test_convert_not_amount(mock_requests_get):
    """Тест для конвертации валюты в RUB когда сумма не передана"""

    mock_requests_get.return_value.json.return_value = {"result": None}

    test_transaction = {"operationAmount": {"amount": "Не число", "currency": {"code": "USD"}}}
    assert convert_transaction(test_transaction) == None
