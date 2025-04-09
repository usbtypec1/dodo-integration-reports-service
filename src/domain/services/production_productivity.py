from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from domain.entities.production_productivity import (
    UnitProductionProductivity,
    UnitProductionProductivityStatistics,
)
from domain.entities.unit import Unit
from domain.services.common import compute_growth_percentage


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductionProductivityService:
    units: Iterable[Unit]
    production_productivities_for_today: Iterable[UnitProductionProductivity]
    production_productivities_for_week_before: Iterable[UnitProductionProductivity]

    def get_production_productivity_statistics(
        self,
    ) -> list[UnitProductionProductivityStatistics]:
        unit_id_to_sales_per_labor_hour_now: dict[UUID, float] = {
            unit.unit_id: unit.sales_per_labor_hour
            for unit in self.production_productivities_for_today
        }
        unit_id_to_sales_per_labor_hour_week_before: dict[UUID, float] = {
            unit.unit_id: unit.sales_per_labor_hour
            for unit in self.production_productivities_for_week_before
        }

        result: list[UnitProductionProductivityStatistics] = []
        for unit in self.units:
            sales_per_labor_hour_for_today = unit_id_to_sales_per_labor_hour_now.get(
                unit.id,
                0.0,
            )
            sales_per_labor_hour_for_week_before = (
                unit_id_to_sales_per_labor_hour_week_before.get(
                    unit.id,
                    0.0,
                )
            )
            growth_percentage = compute_growth_percentage(
                value_now=sales_per_labor_hour_for_today,
                value_then=sales_per_labor_hour_for_week_before,
            )

            result.append(
                UnitProductionProductivityStatistics(
                    unit_name=unit.name,
                    sales_per_labor_hour_for_today=sales_per_labor_hour_for_today,
                    growth_percentage=growth_percentage,
                )
            )

        return result
