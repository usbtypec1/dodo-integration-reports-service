from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from domain.entities.stop_sale_by_sector import (
    StopSaleBySector,
    UnitStopSaleBySector,
    UnitStopSaleBySectorItem,
)
from domain.services.common import group_by_unit_id


@dataclass(frozen=True, slots=True)
class StopSaleBySectorService:
    stop_sales: Iterable[StopSaleBySector]

    def filter_non_resumed_stop_sales(self) -> list[StopSaleBySector]:
        return [
            stop_sale for stop_sale in self.stop_sales if stop_sale.ended_at is None
        ]

    def get_unit_id_to_name(self) -> dict[UUID, str]:
        return {stop_sale.unit_id: stop_sale.unit_name for stop_sale in self.stop_sales}

    def group_by_units(self) -> list[UnitStopSaleBySector]:
        result: list[UnitStopSaleBySector] = []

        unit_id_to_stop_sales = group_by_unit_id(self.stop_sales)
        unit_id_to_name = self.get_unit_id_to_name()

        for unit_id, unit_stop_sales in unit_id_to_stop_sales.items():
            sectors = [
                UnitStopSaleBySectorItem(
                    name=stop_sale.sector_name,
                    started_at=stop_sale.started_at,
                )
                for stop_sale in unit_stop_sales
            ]
            result.append(
                UnitStopSaleBySector(
                    unit_id=unit_id,
                    unit_name=unit_id_to_name[unit_id],
                    sectors=sectors,
                )
            )

        return result
