from dataclasses import dataclass

from domain.entities.account_token import AccountToken
from infrastructure.adapters.gateways.http_client import ApiGatewayHttpClient


@dataclass(frozen=True, slots=True, kw_only=True)
class AccountTokenGateway:
    http_client: ApiGatewayHttpClient

    async def get_account_token(self, account_id: str) -> AccountToken:
        url = f"/v1/accounts/tokens/{account_id}/"
        response = await self.http_client.get(url)
        return AccountToken.model_validate_json(response.text)
