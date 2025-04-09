import itertools
from collections.abc import Iterable
from dataclasses import dataclass
from zoneinfo import ZoneInfo

from application.ports.gateways.dodo_is_api import DodoIsApiGateway
from domain.entities.account_token import AccountTokenUnits
from domain.entities.period import Period
from domain.entities.sales import UnitSalesStatistics
from domain.services.account_token_units import AccountTokenUnitsService
from domain.services.sales import SalesService
from domain.services.unit import UnitService


@dataclass(frozen=True, slots=True, kw_only=True)
class UnitsSalesStatisticsInteractor:
    dodo_is_api_gateway: DodoIsApiGateway
    account_tokens_units: Iterable[AccountTokenUnits]
    timezone: ZoneInfo

    async def execute(self) -> list[UnitSalesStatistics]:
        period_today = Period.today_to_this_time(self.timezone)
        period_week_before = Period.week_before_to_this_time(self.timezone)

        sales_for_today = []
        sales_for_week_before = []

        for account_token_units in self.account_tokens_units:
            for units_batch in itertools.batched(account_token_units.units, n=30):
                sales_for_today += await self.dodo_is_api_gateway.get_units_sales(
                    access_token=account_token_units.access_token.get_secret_value(),
                    unit_ids=UnitService(units_batch).get_unit_ids(),
                    from_date=period_today.from_date,
                    to_date=period_today.to_date,
                )

                sales_for_week_before += await self.dodo_is_api_gateway.get_units_sales(
                    access_token=account_token_units.access_token.get_secret_value(),
                    unit_ids=UnitService(units_batch).get_unit_ids(),
                    from_date=period_week_before.from_date,
                    to_date=period_week_before.to_date,
                )

        units = AccountTokenUnitsService(self.account_tokens_units).get_units()
        sales_service = SalesService(
            units=units,
            sales_for_today=sales_for_today,
            sales_for_week_before=sales_for_week_before,
        )
        return sales_service.get_units_sales_statistics()
