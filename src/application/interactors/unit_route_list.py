from collections import defaultdict
from dataclasses import dataclass
from uuid import UUID

from application.ports.gateways.report_route import ReportRouteGateway
from domain.entities.unit_route import UnitRoute


@dataclass(frozen=True, slots=True, kw_only=True)
class UnitRouteListInteractor:
    report_type_id: str
    report_route_gateway: ReportRouteGateway

    async def execute(self) -> list[UnitRoute]:
        unit_id_to_chat_ids: dict[UUID, set[int]] = defaultdict(set)

        take: int = 1000
        skip: int = 0

        while True:
            response = await self.report_route_gateway.get_report_routes(
                report_type_id=self.report_type_id,
                take=take,
                skip=skip,
            )

            for report_route in response.routes:
                unit_id_to_chat_ids[report_route.unit_id].add(report_route.chat_id)

            if response.is_end_of_list_reached:
                break

            skip += take

        return [
            UnitRoute(
                unit_id=unit_id,
                chat_ids=tuple(chat_ids),
                report_type_id=self.report_type_id,
            )
            for unit_id, chat_ids in unit_id_to_chat_ids.items()
        ]
