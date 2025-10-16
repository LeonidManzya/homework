import pytest

from src.processing import filter_by_state
from src.processing import sort_by_date


def test_filter_by_state(fixture_filter_by_state):
    # Добавляем второй аргумент - состояние "EXECUTED"
    assert filter_by_state(fixture_filter_by_state, "EXECUTED") == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            [
                {"id": 41428829, "date": "2019-07-03T18:35:29.512364", "state": "EXECUTED"},
                {"id": 939719570, "date": "2018-06-30T02:08:58.425572", "state": "CANCELED"},
                {"id": 594226727, "date": "2018-09-12T21:27:25.241689", "state": "PENDING"},
                {"id": 615064591, "date": "2018-10-14T08:21:33.419441", "state": "FAILED"},
            ],
            [],  # Если ищем состояние, которого нет в списке
        )
    ],
)
def test_filter_by_state2(value, expected):
    # Ищем состояние "COMPLETED", которого нет в списке
    assert filter_by_state(value, "COMPLETED") == expected


# Можно добавить больше тестов для разных состояний
@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 2),
        ("PENDING", 0),  # Если такого состояния нет в фикстуре
    ],
)
def test_filter_by_state_different_states(fixture_filter_by_state, state, expected_count):
    result = filter_by_state(fixture_filter_by_state, state)
    assert len(result) == expected_count


def test_sort_by_date(fixture_sort_by_date):
    assert sort_by_date(fixture_sort_by_date) == [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.mark.parametrize(
    "value, expected",
    [([{"date": "2023-10-01"}, {"date": "2023-10-01"}], [{"date": "2023-10-01"}, {"date": "2023-10-01"}])],
)
def test_sort_by_date2(value, expected):
    assert sort_by_date(value) == expected


@pytest.mark.parametrize(
    "input_date, expected_exception",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED"},
                {"id": 939719570, "state": "EXECUTED"},
                {"id": 594226727, "state": "CANCELED"},
                {"id": 615064591, "state": "CANCELED"},
            ],
            KeyError,
        )
    ],
)
def test_sort_by_date3(input_date, expected_exception):
    with pytest.raises(expected_exception):
        sort_by_date(input_date)