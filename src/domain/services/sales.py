from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from domain.entities.sales import UnitSales, UnitSalesStatistics
from domain.entities.unit import Unit


@dataclass(frozen=True, slots=True, kw_only=True)
class SalesService:
    units: Iterable[Unit]
    sales_for_today: Iterable[UnitSales]
    sales_for_week_before: Iterable[UnitSales]

    def get_units_sales_statistics(self) -> list[UnitSalesStatistics]:
        unit_id_to_sales_for_today: dict[UUID, float] = {
            unit_sales.unit_id: unit_sales.sales for unit_sales in self.sales_for_today
        }
        unit_id_to_sales_for_week_before: dict[UUID, float] = {
            unit_sales.unit_id: unit_sales.sales
            for unit_sales in self.sales_for_week_before
        }

        result: list[UnitSalesStatistics] = []
        for unit in self.units:
            sales_for_today = unit_id_to_sales_for_today.get(unit.id, 0)
            sales_for_week_before = unit_id_to_sales_for_week_before.get(unit.id, 0)

            growth_percentage: int = 0
            if sales_for_week_before != 0:
                growth_percentage = round(
                    sales_for_today * 100 / sales_for_week_before - 100
                )

            result.append(
                UnitSalesStatistics(
                    unit_name=unit.name,
                    sales_for_today=sales_for_today,
                    growth_percentage=growth_percentage,
                )
            )
        return result
