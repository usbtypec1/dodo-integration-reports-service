from typing import Annotated

from fast_depends import Depends

from infrastructure.adapters.gateways.http_client import (
    ApiGatewayHttpClientDependency,
)
from infrastructure.adapters.gateways.report_route import ReportRouteGateway


async def report_route_gateway_provider(
    http_client: ApiGatewayHttpClientDependency,
) -> ReportRouteGateway:
    return ReportRouteGateway(http_client=http_client)


ReportRouteGatewayDependency = Annotated[
    ReportRouteGateway,
    Depends(report_route_gateway_provider),
]
