from dataclasses import dataclass
from typing import Iterable

from application.ports.gateways.account_token import AccountTokenGateway
from domain.entities.account_token import AccountToken


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountTokenListInteractor:
    account_ids: Iterable[str]
    account_token_gateway: AccountTokenGateway

    async def execute(self) -> list[AccountToken]:
        account_tokens: list[AccountToken] = []
        for account_id in self.account_ids:
            account_token = await self.account_token_gateway.get_account_token(
                account_id
            )
            account_tokens.append(account_token)
        return account_tokens
