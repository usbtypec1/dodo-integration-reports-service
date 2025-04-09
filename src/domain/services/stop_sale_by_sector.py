from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.stop_sale_by_sector import (
    StopSaleBySector,
    UnitStopSaleBySector,
    UnitStopSaleBySectorItem,
)
from domain.services.common import group_by_unit_name


@dataclass(frozen=True, slots=True)
class StopSaleBySectorService:
    stop_sales: Iterable[StopSaleBySector]

    def filter_non_resumed_stop_sales(self) -> list[StopSaleBySector]:
        return [
            stop_sale for stop_sale in self.stop_sales if stop_sale.ended_at is None
        ]

    def group_by_units(self) -> list[UnitStopSaleBySector]:
        result: list[UnitStopSaleBySector] = []

        unit_name_to_stop_sales = group_by_unit_name(self.stop_sales)

        for unit_name, unit_stop_sales in unit_name_to_stop_sales.items():
            sectors = [
                UnitStopSaleBySectorItem(
                    name=stop_sale.sector_name,
                    started_at=stop_sale.started_at,
                )
                for stop_sale in unit_stop_sales
            ]
            result.append(
                UnitStopSaleBySector(
                    unit_name=unit_name,
                    sectors=sectors,
                )
            )

        return result
