import pytest
import json
import pandas as pd
import os
from tempfile import NamedTemporaryFile
from src.filter_rub_transactions import load_transactions

def test_load_json_file():
    """Тест загрузки JSON файла"""
    with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump([{"id": 1, "amount": 100}], f)
        file_path = f.name

    try:
        result = load_transactions(file_path)
        assert len(result) == 1
        assert result[0]["id"] == 1
    finally:
        os.unlink(file_path)

def test_load_xlsx_file():
    """Тест загрузки XLSX файла"""
    with NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        df = pd.DataFrame([{"id": 1, "amount": 100}])
        df.to_excel(f.name, index=False)
        file_path = f.name

    try:
        result = load_transactions(file_path)
        assert len(result) == 1
        assert result[0]["id"] == '1'
        assert result[0]["amount"] == '100'
    finally:
        os.unlink(file_path)

def test_invalid_file_format():
    """Тест на неподдерживаемый формат файла"""
    with pytest.raises(ValueError, match="Поддерживаются только JSON и XLSX файлы"):
        load_transactions("invalid.csv")