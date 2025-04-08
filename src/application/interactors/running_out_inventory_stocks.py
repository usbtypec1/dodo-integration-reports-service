import itertools
from collections.abc import Iterable
from dataclasses import dataclass

from application.ports.gateways.dodo_is_api import DodoIsApiGateway
from domain.entities.account_token import AccountTokenUnits
from domain.entities.inventory_stocks import (
    InventoryStockItem,
    UnitInventoryStocks,
)
from domain.services.account_token_units import AccountTokenUnitsService
from domain.services.inventory_stocks import InventoryStocksService
from domain.services.unit import UnitService


@dataclass(frozen=True, slots=True, kw_only=True)
class RunningOutInventoryStocksInteractor:
    dodo_is_api_gateway: DodoIsApiGateway
    account_tokens_units: Iterable[AccountTokenUnits]

    async def execute(self) -> list[UnitInventoryStocks]:
        take: int = 1000

        result: list[InventoryStockItem] = []

        for account_token_units in self.account_tokens_units:
            for units_batch in itertools.batched(account_token_units.units, n=30):
                skip: int = 0

                while True:
                    unit_service = UnitService(units=units_batch)
                    response = await self.dodo_is_api_gateway.get_inventory_stocks(
                        access_token=account_token_units.access_token.get_secret_value(),
                        unit_ids=unit_service.get_unit_ids(),
                        take=take,
                        skip=skip,
                    )
                    inventory_stocks_service = InventoryStocksService(response.stocks)
                    result += inventory_stocks_service.filter_running_out_stocks(
                        days_until_balance_runs_out=1,
                    )

                    if response.is_end_of_list_reached:
                        break

                    skip += take

        account_token_units_service = AccountTokenUnitsService(
            self.account_tokens_units
        )
        unit_id_to_name = account_token_units_service.get_unit_id_to_name()
        inventory_stocks_service = InventoryStocksService(result)
        return inventory_stocks_service.group_by_unit_id(unit_id_to_name)
