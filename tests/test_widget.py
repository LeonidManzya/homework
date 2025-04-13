import pytest

from src.widget import get_date
from src.widget import mask_account_card


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa Gold 599941422", "Visa Gold Проверьте правильность введенного номера карты!"),
        ("Счет 6468647367889477958900", "Счет Проверьте правильность введенного номера счёта!"),
    ],
)
def test_mask_account_card(value, expected):
    assert mask_account_card(value) == expected


@pytest.mark.parametrize(
    "value, expected", [("2024-03-11T02:26:18.671407", "11.03.2024"), ("2025-04-01T14:05:23.817521", "01.04.2025")]
)
def test_get_date(value, expected):
    assert get_date(value) == expected


@pytest.mark.parametrize(
    "input_date, expected_exception", [("2024-33-11T02:26:18.671407", ValueError), ("247593774082384", ValueError)]
)
def test_get_date_exceptions(input_date, expected_exception):
    with pytest.raises(expected_exception):
        get_date(input_date)
