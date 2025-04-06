from typing import Annotated

from fast_depends import Depends

from infrastructure.adapters.gateways.http_client import (
    ApiGatewayHttpClientDependency,
)
from infrastructure.adapters.gateways.unit import UnitGateway


async def unit_gateway_provider(
    http_client: ApiGatewayHttpClientDependency,
) -> UnitGateway:
    return UnitGateway(http_client=http_client)


UnitGatewayDependency = Annotated[
    UnitGateway,
    Depends(unit_gateway_provider),
]
