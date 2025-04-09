import asyncio
import itertools
from collections.abc import Iterable
from dataclasses import dataclass
from zoneinfo import ZoneInfo

from application.ports.gateways.dodo_is_api import DodoIsApiGateway
from domain.entities.account_token import AccountTokenUnits
from domain.entities.period import Period
from domain.entities.production_productivity import (
    UnitProductionProductivity,
    UnitProductionProductivityStatistics,
)
from domain.services.account_token_units import AccountTokenUnitsService
from domain.services.production_productivity import (
    ProductionProductivityService,
)
from domain.services.unit import UnitService


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductionProductivityInteractor:
    dodo_is_api_gateway: DodoIsApiGateway
    account_tokens_units: Iterable[AccountTokenUnits]
    timezone: ZoneInfo

    async def execute(self) -> list[UnitProductionProductivityStatistics]:
        period_today = Period.today_to_this_time(self.timezone).round_to_upper_hour()
        period_week_before = Period.week_before_to_this_time(
            self.timezone
        ).round_to_upper_hour()

        production_productivities_for_today: list[UnitProductionProductivity] = []
        production_productivities_for_week_before: list[UnitProductionProductivity] = []

        for account_token_units in self.account_tokens_units:
            for units_batch in itertools.batched(
                account_token_units.units,
                n=30,
            ):
                unit_ids = UnitService(units_batch).get_unit_ids()

                async with asyncio.TaskGroup() as task_group:
                    production_productivity_for_today_task = task_group.create_task(
                        self.dodo_is_api_gateway.get_production_productivity(
                            access_token=account_token_units.access_token.get_secret_value(),
                            from_date=period_today.from_date,
                            to_date=period_today.to_date,
                            unit_ids=unit_ids,
                        )
                    )
                    production_productivity_for_week_before_task = task_group.create_task(
                        self.dodo_is_api_gateway.get_production_productivity(
                            access_token=account_token_units.access_token.get_secret_value(),
                            from_date=period_week_before.from_date,
                            to_date=period_week_before.to_date,
                            unit_ids=unit_ids,
                        )
                    )

                production_productivities_for_today += (
                    production_productivity_for_today_task.result()
                )
                production_productivities_for_week_before += (
                    production_productivity_for_week_before_task.result()
                )

        units = AccountTokenUnitsService(self.account_tokens_units).get_units()
        production_productivity_service = ProductionProductivityService(
            units=units,
            production_productivities_for_today=production_productivities_for_today,
            production_productivities_for_week_before=production_productivities_for_week_before,
        )
        return production_productivity_service.get_production_productivity_statistics()
