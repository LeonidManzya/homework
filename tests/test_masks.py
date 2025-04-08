import pytest
from src.masks import get_mask_card_number, get_mask_account_number

"""""Тест функции маски номера карты"""

def test_get_mask_card_number(fixture_number_card):
    assert get_mask_card_number(fixture_number_card) == '9485 21** **** 4653'

@pytest.mark.parametrize('value, expected', [('094852134087746530', "Проверьте правильность введенного номера карты!"), ('', "Проверьте правильность введенного номера карты!")])
def test_get_mask_card_number(value, expected):
    assert get_mask_card_number(value) == expected

"""Тест функции маски номера счёта"""

def test_get_mask_account_number(fixture_number_account):
    assert get_mask_account_number(fixture_number_account) == '**4455'

@pytest.mark.parametrize('value, expected', [('084s382374f332277a4550', "Проверьте правильность введенного номера счёта!"), ('846382374', "Проверьте правильность введенного номера счёта!"), ('', "Проверьте правильность введенного номера счёта!")])
def test_get_mask_account_number(value, expected):
    assert get_mask_account_number(value) == expected



