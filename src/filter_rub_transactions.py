import json
import pandas as pd
from typing import List, Dict, Any


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, engine='openpyxl', dtype=str, na_values=[''])
        df = df.where(pd.notnull(df), None)
        return df.to_dict('records')
    else:
        raise ValueError("Поддерживаются только JSON и XLSX файлы")


def is_rub_currency(value: Any) -> bool:
    if not value:
        return False

    value_str = str(value).upper()
    rub_indicators = ['RUB', 'РУБ', 'RUR', '₽', 'РУБЛЬ', 'РУБЛЕЙ']
    return any(indicator in value_str for indicator in rub_indicators)


def find_currency_value(transaction: Dict[str, Any]) -> Any:
    if 'currency' in transaction:
        return transaction['currency']
    if 'operationAmount' in transaction and isinstance(transaction['operationAmount'], dict):
        return transaction['operationAmount'].get('currency')

    for key in transaction.keys():
        if 'currency' in str(key).lower():
            return transaction[key]

    return None


def filter_rub_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rub_transactions = []

    for tr in transactions:
        currency = find_currency_value(tr)

        if isinstance(currency, dict):
            currency = currency.get('code') or currency.get('name') or str(currency)

        if is_rub_currency(currency):
            rub_transactions.append(tr)

    return rub_transactions


