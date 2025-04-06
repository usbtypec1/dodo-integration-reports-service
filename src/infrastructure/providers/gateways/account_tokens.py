from typing import Annotated

from fast_depends import Depends

from infrastructure.adapters.gateways.http_client import (
    ApiGatewayHttpClientDependency,
)
from infrastructure.adapters.gateways.account_token import AccountTokenGateway


async def account_token_gateway_provider(
    http_client: ApiGatewayHttpClientDependency,
) -> AccountTokenGateway:
    return AccountTokenGateway(http_client=http_client)


AccountTokenGatewayDependency = Annotated[
    AccountTokenGateway,
    Depends(account_token_gateway_provider),
]
