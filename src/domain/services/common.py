from collections import defaultdict
from collections.abc import Iterable
from typing import Protocol
from uuid import UUID


def compute_growth_percentage(
    value_now: int | float,
    value_then: int | float,
) -> int:
    if value_then == 0:
        return 0
    return round((value_now - value_then) / value_then * 100)


class HasUnitId(Protocol):
    unit_id: UUID


def group_by_unit_id[T: HasUnitId](
    items: Iterable[T],
) -> dict[UUID, list[T]]:
    unit_id_to_items = defaultdict(list)
    for item in items:
        unit_id_to_items[item.unit_id].append(item)
    return dict(unit_id_to_items)
