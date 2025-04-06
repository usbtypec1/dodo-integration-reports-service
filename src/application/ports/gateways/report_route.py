from typing import Protocol

from domain.entities.report_route import ReportRoute


class ReportRouteGateway(Protocol):
    async def get_report_routes(
        self,
        *,
        report_type_id: str,
        chat_id: int,
    ) -> list[ReportRoute]: ...
