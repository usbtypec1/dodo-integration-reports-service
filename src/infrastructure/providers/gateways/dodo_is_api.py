from typing import Annotated

from fast_depends import Depends

from infrastructure.adapters.gateways.dodo_is_api import DodoIsApiGateway
from infrastructure.adapters.gateways.http_client import (
    DodoIsApiGatewayHttpClientDependency,
)


async def dodo_is_api_gateway_provider(
    http_client: DodoIsApiGatewayHttpClientDependency,
) -> DodoIsApiGateway:
    return DodoIsApiGateway(http_client=http_client)


DodoIsApiGatewayDependency = Annotated[
    DodoIsApiGateway,
    Depends(dodo_is_api_gateway_provider),
]
