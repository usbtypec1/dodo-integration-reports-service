import contextlib
from collections.abc import AsyncGenerator
from typing import Annotated, NewType

import httpx
from fast_depends import Depends

from bootstrap.config import Config
from infrastructure.providers.config import ConfigDependency

DodoIsApiGatewayHttpClient = NewType(
    "DodoIsApiGatewayHttpClient",
    httpx.AsyncClient,
)

ApiGatewayHttpClient = NewType(
    "ApiGatewayHttpClient",
    httpx.AsyncClient,
)


async def create_dodo_is_api_gateway_http_client(
    *,
    config: ConfigDependency,
) -> AsyncGenerator[DodoIsApiGatewayHttpClient, None]:
    async with httpx.AsyncClient(
        base_url=config.dodo_is_api_gateway_base_url,
    ) as http_client:
        yield DodoIsApiGatewayHttpClient(http_client)


async def create_api_gateway_http_client(
    *,
    config: ConfigDependency,
) -> AsyncGenerator[ApiGatewayHttpClient, None]:
    headers = {"Authorization": f"Bearer {config.api_gateway_token}"}
    async with httpx.AsyncClient(
        base_url=config.api_gateway_base_url,
        headers=headers,
    ) as http_client:
        yield ApiGatewayHttpClient(http_client)


DodoIsApiGatewayHttpClientDependency = Annotated[
    DodoIsApiGatewayHttpClient,
    Depends(create_dodo_is_api_gateway_http_client),
]


ApiGatewayHttpClientDependency = Annotated[
    ApiGatewayHttpClient,
    Depends(create_api_gateway_http_client),
]
