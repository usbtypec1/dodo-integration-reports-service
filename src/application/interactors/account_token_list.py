from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from application.ports.gateways.account_token import AccountTokenGateway
from domain.entities.account_token import AccountToken, AccountTokenUnits
from domain.entities.chat_route import ChatRoute
from domain.entities.unit import Unit
from domain.services.unit import UnitService


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountTokenListInteractor:
    units: Iterable[Unit]
    chat_routes: Iterable[ChatRoute] | None = None
    account_token_gateway: AccountTokenGateway

    async def execute(self) -> list[AccountTokenUnits]:
        if self.chat_routes is not None:
            unit_ids_to_request_account_tokens: set[UUID] = {
                unit_id
                for chat_route in self.chat_routes
                for unit_id in chat_route.unit_ids
            }
            units_to_request_account_tokens = [
                unit
                for unit in self.units
                if unit.id in unit_ids_to_request_account_tokens
            ]
        else:
            units_to_request_account_tokens = self.units
        unit_service = UnitService(units=units_to_request_account_tokens)
        account_ids = unit_service.get_dodo_is_api_account_ids()

        account_tokens: list[AccountToken] = []
        for account_id in account_ids:
            account_token = await self.account_token_gateway.get_account_token(
                account_id
            )
            account_tokens.append(account_token)

        return unit_service.combine_with_account_tokens(account_tokens)
