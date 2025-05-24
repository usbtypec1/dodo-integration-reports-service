from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID
from zoneinfo import ZoneInfo

from application.ports.gateways.stop_sales_cache import StopSalesCacheGateway
from domain.entities.stop_sale_by_ingredient import (
    StopSaleByIngredient,
    UnitStopSalesByIngredientItem,
    UnitStopSalesByIngredients,
    UnitStopSalesByIngredientsByReasons,
)
from domain.services.common import group_by_unit_id


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

    def get_unit_id_to_name(self) -> dict[UUID, str]:
        return {stop_sale.unit_id: stop_sale.unit_name for stop_sale in self.stop_sales}

    def group_by_units_and_reasons(
        self, timezone: ZoneInfo
    ) -> list[UnitStopSalesByIngredients]:
        result: list[UnitStopSalesByIngredients] = []

        unit_id_to_stop_sales = group_by_unit_id(self.stop_sales)
        unit_id_to_name = self.get_unit_id_to_name()

        for unit_id, unit_stop_sales in unit_id_to_stop_sales.items():
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
                    unit_id=unit_id,
                    unit_name=unit_id_to_name[unit_id],
                    ingredients_by_reasons=ingredients_by_reasons,
                    timezone=timezone.key,
                )
            )

        return result

    async def filter_non_existing_stop_sales(
        self,
        cache: StopSalesCacheGateway,
    ) -> list[StopSaleByIngredient]:
        """
        Filters stop sales that do not exist in the cache.

        Args:
            cache (StopSalesCacheGateway): The cache gateway to check for existence.

        Returns:
            list[StopSaleByIngredient]: A list of stop sales that exist in the cache.
        """
        return [
            stop_sale
            for stop_sale in self.stop_sales
            if not await cache.exists(stop_sale.id)
        ]
