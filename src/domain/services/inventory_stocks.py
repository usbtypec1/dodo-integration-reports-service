from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from uuid import UUID

from domain.entities.inventory_stocks import (
    InventoryStockItem,
    UnitInventoryStockItem,
    UnitInventoryStocks,
)


@dataclass(frozen=True, slots=True)
class InventoryStocksService:
    stocks: Iterable[InventoryStockItem]

    def filter_running_out_stocks(
        self, days_until_balance_runs_out: int
    ) -> list[InventoryStockItem]:
        return [
            stock
            for stock in self.stocks
            if stock.days_until_balance_runs_out <= days_until_balance_runs_out
        ]

    def group_by_unit_id(
        self,
        unit_id_to_name: Mapping[UUID, str],
    ) -> list[UnitInventoryStocks]:
        unit_id_to_stock_items: dict[UUID, list[UnitInventoryStockItem]] = defaultdict(
            list
        )

        for stock_item in self.stocks:
            item = UnitInventoryStockItem(
                name=stock_item.name,
                quantity=stock_item.quantity,
                measurement_unit=stock_item.measurement_unit,
            )
            unit_id_to_stock_items[stock_item.unit_id].append(item)

        return [
            UnitInventoryStocks(
                unit_name=unit_id_to_name.get(unit_id, unit_id.hex),
                items=items,
            )
            for unit_id, items in unit_id_to_stock_items.items()
        ]
