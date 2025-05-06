import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions


@pytest.mark.parametrize(
    "currency, expected",
    [
        (
            "USD",
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
                {
                    "id": 895315941,
                    "state": "EXECUTED",
                    "date": "2018-08-19T04:27:37.904916",
                    "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод с карты на карту",
                    "from": "Visa Classic 6831982476737658",
                    "to": "Visa Platinum 8990922113665229",
                },
            ],
        ),
        (
            "RUB",
            [
                {
                    "id": 873106923,
                    "state": "EXECUTED",
                    "date": "2019-03-23T01:09:46.296404",
                    "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                },
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                    "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод организации",
                    "from": "Visa Platinum 1246377376343588",
                    "to": "Счет 14211924144426031657",
                },
            ],
        ),
    ],
)
def test_filter_by_currency1(make_transactions1: list, currency: str, expected: list) -> None:
    """Тест для функции фильтрации по коду валюты - норма"""
    assert list(filter_by_currency(make_transactions1, currency)) == expected


@pytest.mark.parametrize(
    "currency, expected", [("USD", "Отсутствуют данные для обработки"), ("RUB", "Отсутствуют данные для обработки")]
)
def test_filter_by_currency2(make_transactions2: list, currency: str, expected: list) -> None:
    """Тест для функции фильтрации по коду валюты - пустой список для обработки"""
    result = "".join(filter_by_currency(make_transactions2, currency))
    assert result == expected


@pytest.mark.parametrize(
    "currency, expected",
    [
        ("USD", "Для одной или нескольких транзакций значение валюты не задано"),
        ("RUB", "Для одной или нескольких транзакций значение валюты не задано"),
    ],
)
def test_filter_by_currency3(make_transactions3: list, currency: str, expected: list) -> None:
    """Тест для функции фильтрации по коду валюты -
    'operationAmount' не является словарем"""
    result = "".join(filter_by_currency(make_transactions3, currency))
    assert result == expected


@pytest.mark.parametrize(
    "currency, expected",
    [
        ("USD", "Для одной или нескольких транзакций значение валюты не задано"),
        ("RUB", "Для одной или нескольких транзакций значение валюты не задано"),
    ],
)
def test_filter_by_currency4(make_transactions4: list, currency: str, expected: list) -> None:
    """Тест для функции фильтрации по коду валюты -
    нет ключа currency в одном из словарей"""
    result = "".join(filter_by_currency(make_transactions4, currency))
    assert result == expected


@pytest.mark.parametrize(
    "currency, expected",
    [
        ("USD", "Для одной или нескольких транзакций значение валюты не задано"),
        ("RUB", "Для одной или нескольких транзакций значение валюты не задано"),
    ],
)
def test_filter_by_currency5(make_transactions5: list, currency: str, expected: list) -> None:
    """Тест для функции фильтрации по коду валюты -
    нет ключа "operationAmount" в одном из словарей"""
    result = "".join(filter_by_currency(make_transactions5, currency))
    assert result == expected


@pytest.mark.parametrize(
    "currency, expected",
    [
        ("CNY", "В списке отсутствуют транзакции с данной валютой"),
        ("EUR", "В списке отсутствуют транзакции с данной валютой"),
    ],
)
def test_filter_by_currency6(make_transactions1: list, currency: str, expected: list) -> None:
    """Тест для функции фильтрации по коду валюты -
    в обрабатываемом списке нет операций с заданной валютой"""
    result = "".join(filter_by_currency(make_transactions1, currency))
    assert result == expected


def test_transaction_descriptions1(make_transactions1: list, make_descriptions1: list) -> None:
    """Тест для функции получения описаний транзакций - норма"""
    assert list(transaction_descriptions(make_transactions1)) == list(make_descriptions1)


def test_transaction_descriptions2(make_transactions2: list) -> None:
    """Тест для функции получения описаний транзакций - обработка пустого списка"""
    result = "".join(transaction_descriptions(make_transactions2))
    assert result == "Отсутствуют данные для обработки"


def test_transaction_descriptions3(make_transactions3: list, make_descriptions3: list) -> None:
    """Тест для функции получения описаний транзакций -
    в одном из словарей отсутствует ключ "description" """
    result = list(transaction_descriptions(make_transactions3))
    assert result == make_descriptions3


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 2, ["0000 0000 0000 0001"]),
        (
            1,
            6,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
    ],
)
def test_card_number_generator1(start: int, stop: int, expected: list) -> None:
    """Тест для генератора номеров карт - норма"""
    assert list(card_number_generator(start, stop)) == expected


def test_card_number_generator2() -> None:
    """Тест для генератора номеров карт - начало диапазона меньше, чем конец"""
    with pytest.raises(ValueError, match="Ошибка: начальное значение должно быть меньше конечного!"):
        list(card_number_generator(6, 4))


def test_card_number_generator3() -> None:
    """Тест для генератора номеров карт - начало диапазона меньше нуля"""
    with pytest.raises(ValueError, match="Ошибка при вводе значений границ диапазона!"):
        list(card_number_generator((-6), 4))


def test_card_number_generator4() -> None:
    """Тест для генератора номеров карт - для start введено нецифровое значение"""
    with pytest.raises(TypeError, match="Неверный формат данных!"):
        list(card_number_generator("1", 4))


def test_card_number_generator5() -> None:
    """Тест для генератора номеров карт - граница диапазона обозначена
    числом с количеством разрядов больше 16"""
    with pytest.raises(ValueError, match="Ошибка при вводе значений границ диапазона!"):
        list(card_number_generator(5, 4785694356489535864))


def test_card_number_generator6() -> None:
    """Тест для генератора номеров карт - начало и конец диапазона совпадают,
    генератор не может создать ни одного значения"""
    with pytest.raises(ValueError, match="Ошибка: начальное значение должно быть меньше конечного!"):
        list(card_number_generator(4, 4))


def test_card_number_generator7() -> None:
    """Тест для генератора номеров карт - обработка крайних значений,
    просчет количества нулей при изменении разрядности"""
    result = list(card_number_generator(99, 101))
    assert result[0] == "0000 0000 0000 0099"
    assert result[1] == "0000 0000 0000 0100"
    assert "0000 0000 0000 0101" not in result
