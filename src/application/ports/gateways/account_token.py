from typing import Protocol

from domain.entities.account_token import AccountToken


class AccountTokenGateway(Protocol):
    async def get_account_token(self, account_id: str) -> AccountToken: ...
