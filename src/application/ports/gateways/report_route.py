from collections.abc import Iterable
from typing import Protocol

from domain.entities.report_route import ReportRouteListResponse


class ReportRouteGateway(Protocol):
    async def get_report_routes(
        self,
        *,
        report_type_id: str,
        chat_ids: Iterable[int],
    ) -> ReportRouteListResponse: ...
