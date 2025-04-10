from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from domain.entities.sales import (
    SalesStatistics,
    TotalSalesStatistics,
    UnitSales,
    UnitSalesStatistics,
)
from domain.entities.unit import Unit
from domain.services.common import compute_growth_percentage


@dataclass(frozen=True, slots=True, kw_only=True)
class SalesService:
    units: Iterable[Unit]
    sales_for_today: Iterable[UnitSales]
    sales_for_week_before: Iterable[UnitSales]

    def get_total_statistics(self) -> TotalSalesStatistics:
        total_sales_for_today = sum(
            unit_sales.sales for unit_sales in self.sales_for_today
        )
        total_sales_for_week_before = sum(
            unit_sales.sales for unit_sales in self.sales_for_week_before
        )

        growth_percentage = compute_growth_percentage(
            value_now=total_sales_for_today,
            value_then=total_sales_for_week_before,
        )

        return TotalSalesStatistics(
            sales_for_today=total_sales_for_today,
            growth_percentage=growth_percentage,
        )

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

            growth_percentage = compute_growth_percentage(
                value_now=sales_for_today,
                value_then=sales_for_week_before,
            )

            result.append(
                UnitSalesStatistics(
                    unit_name=unit.name,
                    sales_for_today=sales_for_today,
                    growth_percentage=growth_percentage,
                )
            )
        return result

    def get_sales_statistics(self) -> SalesStatistics:
        return SalesStatistics(
            units_breakdown=self.get_units_sales_statistics(),
            total=self.get_total_statistics(),
        )
