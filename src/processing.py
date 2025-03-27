def filter_by_state(opiration: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению."""

    return [item for item in opiration if item.get("state") == state]


def sort_be_date(operation: list[dict], flow: bool = True) -> list[dict]:
    """Функция возвращает новый список, отсортированный по дате."""

    return sorted(operation, key=lambda item: item["date"], reverse=flow)
