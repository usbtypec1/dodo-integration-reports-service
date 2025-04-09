from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.stop_sale_by_sales_channel import (
    StopSaleBySalesChannel,
    UnitStopSaleBySalesChannel,
)


@dataclass(frozen=True, slots=True)
class StopSaleBySalesChannelService:
    stop_sales: Iterable[StopSaleBySalesChannel]

    def filter_not_resumed_stop_sales(self) -> list[StopSaleBySalesChannel]:
        return [
            stop_sale
            for stop_sale in self.stop_sales
            if stop_sale.ended_at_local is None
        ]

    def get_unit_stop_sales(self) -> list[UnitStopSaleBySalesChannel]:
        return [
            UnitStopSaleBySalesChannel(
                unit_name=stop_sale.unit_name,
                started_at=stop_sale.started_at_local,
                sales_channel_name=stop_sale.sales_channel_name,
                reason=stop_sale.reason,
            )
            for stop_sale in self.stop_sales
        ]
