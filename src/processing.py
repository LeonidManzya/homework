def filter_by_state(operation: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению."""

    return [item for item in operation if item.get("state") == state]


def sort_by_date(operation: list[dict], flow: bool = True) -> list[dict]:
    """Функция возвращает новый список, отсортированный по дате."""
    try:
        return sorted(operation, key=lambda item: item["date"], reverse=flow)
    except KeyError:
        print("Неверный формат даты")
        raise KeyError("Неверный формат даты")
