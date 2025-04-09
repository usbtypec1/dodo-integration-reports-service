from collections import defaultdict
from collections.abc import Iterable
from typing import Protocol


def compute_growth_percentage(
    value_now: int | float,
    value_then: int | float,
) -> int:
    if value_then == 0:
        return 0
    return round((value_now - value_then) / value_then * 100)


class HasUnitName(Protocol):
    unit_name: str


def group_by_unit_name[T: HasUnitName](
    stop_sales: Iterable[T],
) -> dict[str, list[T]]:
    unit_name_to_stop_sales = defaultdict(list)
    for stop_sale in stop_sales:
        unit_name_to_stop_sales[stop_sale.unit_name].append(stop_sale)
    return dict(unit_name_to_stop_sales)
