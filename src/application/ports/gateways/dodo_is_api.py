import datetime
from collections.abc import Iterable
from typing import Protocol
from uuid import UUID

from domain.entities.inventory_stocks import InventoryStocksResponse
from domain.entities.late_delivery_voucher import LateDeliveryVouchersResponse


class DodoIsApiGateway(Protocol):
    async def get_late_delivery_vouchers(
        self,
        *,
        access_token: str,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        unit_ids: Iterable[UUID],
        take: int | None = None,
        skip: int | None = None,
    ) -> LateDeliveryVouchersResponse: ...

    async def get_inventory_stocks(
        self,
        *,
        access_token: str,
        unit_ids: Iterable[UUID],
        take: int | None = None,
        skip: int | None = None,
    ) -> InventoryStocksResponse: ...
