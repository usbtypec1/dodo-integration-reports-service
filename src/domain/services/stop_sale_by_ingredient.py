from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.stop_sale_by_ingredient import (
    StopSaleByIngredient,
    UnitStopSalesByIngredientItem,
    UnitStopSalesByIngredients,
    UnitStopSalesByIngredientsByReasons,
)
from domain.services.common import group_by_unit_name


def group_by_reason(
    stop_sales: Iterable[StopSaleByIngredient],
) -> dict[str, list[StopSaleByIngredient]]:
    reason_to_stop_sales = defaultdict(list)
    for stop_sale in stop_sales:
        reason_to_stop_sales[stop_sale.reason].append(stop_sale)
    return dict(reason_to_stop_sales)


@dataclass(frozen=True, slots=True)
class StopSaleByIngredientService:
    stop_sales: Iterable[StopSaleByIngredient]

    def filter_non_resumed_stop_sales(self) -> list[StopSaleByIngredient]:
        return [
            stop_sale
            for stop_sale in self.stop_sales
            if stop_sale.ended_at_local is None
        ]

    def group_by_units_and_reasons(self) -> list[UnitStopSalesByIngredients]:
        result: list[UnitStopSalesByIngredients] = []

        unit_name_to_stop_sales = group_by_unit_name(self.stop_sales)

        for unit_name, unit_stop_sales in unit_name_to_stop_sales.items():
            reason_to_stop_sales = group_by_reason(unit_stop_sales)

            ingredients_by_reasons = []
            for reason, reason_stop_sales in reason_to_stop_sales.items():
                ingredients = [
                    UnitStopSalesByIngredientItem(
                        name=stop_sale.ingredient_name,
                        started_at=stop_sale.started_at_local,
                    )
                    for stop_sale in reason_stop_sales
                ]
                ingredients_by_reason = UnitStopSalesByIngredientsByReasons(
                    reason=reason,
                    ingredients=ingredients,
                )
                ingredients_by_reasons.append(ingredients_by_reason)

            result.append(
                UnitStopSalesByIngredients(
                    unit_name=unit_name,
                    ingredients_by_reasons=ingredients_by_reasons,
                )
            )

        return result
