from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.report_route import ReportRouteListResponse
from infrastructure.adapters.gateways.http_client import (
    ApiGatewayHttpClient,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class ReportRouteGateway:
    http_client: ApiGatewayHttpClient

    async def get_report_routes(
        self,
        *,
        report_type_id: str,
        chat_ids: Iterable[int] | None = None,
    ) -> ReportRouteListResponse:
        url = "/v1/reports/routes/"
        query_params: dict = {"report_type_id": report_type_id}
        if chat_ids is not None:
            query_params["chat_ids"] = chat_ids
        response = await self.http_client.get(url, params=query_params)
        return ReportRouteListResponse.model_validate_json(response.text)
