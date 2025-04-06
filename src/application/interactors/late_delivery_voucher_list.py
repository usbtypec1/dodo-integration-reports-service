from collections.abc import Iterable
import datetime
from dataclasses import dataclass
from uuid import UUID
import itertools

from application.ports.gateways.dodo_is_api import DodoIsApiGateway
from domain.entities.late_delivery_voucher import LateDeliveryVoucher


@dataclass(frozen=True, slots=True, kw_only=True)
class LateDeliveryVoucherListInteractor:
    dodo_is_api_gateway: DodoIsApiGateway
    from_date: datetime.datetime
    to_date: datetime.datetime
    unit_ids: Iterable[UUID]
    access_token: str

    async def execute(self) -> list[LateDeliveryVoucher]:
        take: int = 1000

        late_delivery_vouchers: list[LateDeliveryVoucher] = []
        for unit_ids_batch in itertools.batched(self.unit_ids, n=30):
            skip: int = 0
            while True:
                response = (
                    await self.dodo_is_api_gateway.get_late_delivery_vouchers(
                        access_token=self.access_token,
                        from_date=self.from_date,
                        to_date=self.to_date,
                        unit_ids=unit_ids_batch,
                        take=take,
                        skip=skip,
                    )
                )
                late_delivery_vouchers += response.vouchers
                if response.is_end_of_list_reached:
                    break

            skip += take

        return late_delivery_vouchers
