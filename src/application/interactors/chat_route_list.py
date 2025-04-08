import itertools
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from application.ports.gateways.report_route import ReportRouteGateway
from domain.entities.chat_route import ChatRoute


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatRouteListInteractor:
    report_type_id: str
    chat_ids: Iterable[int]
    report_route_gateway: ReportRouteGateway

    async def execute(self) -> list[ChatRoute]:
        chat_id_to_unit_ids: dict[int, set[UUID]] = defaultdict(set)

        take: int = 1000
        for chat_ids_batch in itertools.batched(self.chat_ids, n=100):
            skip: int = 0

            while True:
                response = await self.report_route_gateway.get_report_routes(
                    report_type_id=self.report_type_id,
                    chat_ids=chat_ids_batch,
                )

                for report_route in response.routes:
                    chat_id_to_unit_ids[report_route.chat_id].add(report_route.unit_id)

                if response.is_end_of_list_reached:
                    break

                skip += take

        return [
            ChatRoute(
                chat_id=chat_id,
                unit_ids=tuple(unit_ids),
                report_type_id=self.report_type_id,
            )
            for chat_id, unit_ids in chat_id_to_unit_ids.items()
        ]
