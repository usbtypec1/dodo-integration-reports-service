import itertools
from collections.abc import Iterable
from dataclasses import dataclass
from zoneinfo import ZoneInfo

from application.ports.gateways.dodo_is_api import DodoIsApiGateway
from domain.entities.account_token import AccountTokenUnits
from domain.entities.period import Period
from domain.entities.stop_sale_by_sector import (
    StopSaleBySector,
    UnitStopSalesBySectors,
)
from domain.services.stop_sale_by_sector import StopSaleBySectorService
from domain.services.unit import UnitService


@dataclass(frozen=True, slots=True, kw_only=True)
class StopSalesBySectorsInteractor:
    dodo_is_api_gateway: DodoIsApiGateway
    account_tokens_units: Iterable[AccountTokenUnits]
    timezone: ZoneInfo

    async def execute(self) -> list[UnitStopSalesBySectors]:
        period = Period.today_to_this_time(self.timezone)

        stop_sales: list[StopSaleBySector] = []

        for account_token_units in self.account_tokens_units:
            for units_batch in itertools.batched(
                account_token_units.units,
                n=30,
            ):
                unit_service = UnitService(units_batch)
                units_stop_sales = await self.dodo_is_api_gateway.get_stop_sales_by_sectors(
                    access_token=account_token_units.access_token.get_secret_value(),
                    unit_ids=unit_service.get_unit_ids(),
                    from_date=period.from_date,
                    to_date=period.to_date,
                )
                stop_sales += StopSaleBySectorService(
                    stop_sales=units_stop_sales
                ).filter_non_resumed_stop_sales()

        return StopSaleBySectorService(stop_sales=stop_sales).group_by_units(
            timezone=self.timezone,
        )
