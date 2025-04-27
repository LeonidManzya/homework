import os
import tempfile

import pytest

from src.decorators import log


def test_log_1(capsys: pytest.CaptureFixture[str]) -> None:

    @log()
    def add_nums(x: int, y: int) -> int:
        return x + y

    add_nums(1, 2)
    captured = capsys.readouterr()
    result = captured.out.split("\n")
    time_result = " ".join((result[1].split(" "))[:2])
    assert result[0] == "add_nums started with arguments: (1, 2), {}"
    assert time_result == "Execution time:"
    assert result[2] == "add_nums ended -> OK"
    assert result[3] == "Results: 3"


def test_log_2(capsys: pytest.CaptureFixture[str]) -> None:

    @log()
    def division_nums(x: int, y: int) -> int | float:
        return x / y

    division_nums(1, 0)
    captured = capsys.readouterr()
    result = captured.out.split("\n")
    time_result = " ".join((result[4].split(" "))[:4])
    assert result[0] == "division_nums started with arguments: (1, 0), {}"
    assert result[1] == "division_nums raised an error"
    assert result[2] == "Error type: ZeroDivisionError"
    assert result[3] == "Error message: division by zero"
    assert time_result == "Execution time before error:"


def test_log_3(capsys: pytest.CaptureFixture[str]) -> None:

    @log()
    def division_nums(x: int, y: int) -> int | float:
        return x / y

    division_nums(1, "1")
    captured = capsys.readouterr()
    result = captured.out.split("\n")
    time_result = " ".join((result[4].split(" "))[:4])
    assert result[0] == "division_nums started with arguments: (1, '1'), {}"
    assert result[1] == "division_nums raised an error"
    assert result[2] == "Error type: TypeError"
    assert result[3] == "Error message: unsupported operand type(s) for /: 'int' and 'str'"
    assert time_result == "Execution time before error:"


def test_log_4() -> None:

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        filename = temp_file.name
    try:

        @log(filename=filename)
        def add_nums(x: int, y: int) -> int:
            return x + y

        add_nums(1, 2)
        with open(filename, "r") as file:
            result = file.readlines()
            time_result = " ".join((result[1].split(" "))[:2])
            assert result[0] == "add_nums started with arguments: (1, 2), {}\n"
            assert time_result == "Execution time:"
            assert result[2] == "add_nums ended -> OK\n"
            assert result[3] == "Results: 3\n"

    finally:
        if os.path.exists(filename):
            os.remove(filename)


def test_log_5() -> None:

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        filename = temp_file.name
    try:

        @log(filename=filename)
        def division_nums(x: int, y: int) -> int | float:
            return x / y

        division_nums(1, 0)
        with open(filename, "r") as file:
            result = file.readlines()
            time_result = " ".join((result[4].split(" "))[:4])
            assert result[0] == "division_nums started with arguments: (1, 0), {}\n"
            assert result[1] == "division_nums raised an error\n"
            assert result[2] == "Error type: ZeroDivisionError\n"
            assert result[3] == "Error message: division by zero\n"
            assert time_result == "Execution time before error:"
    finally:
        if os.path.exists(filename):
            os.remove(filename)
