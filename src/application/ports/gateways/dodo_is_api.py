import datetime
from collections.abc import Iterable
from typing import Protocol
from uuid import UUID

from domain.entities.inventory_stocks import InventoryStocksResponse
from domain.entities.late_delivery_voucher import LateDeliveryVouchersResponse
from domain.entities.production_productivity import UnitProductionProductivity
from domain.entities.sales import UnitSales
from domain.entities.stop_sale_by_ingredient import StopSaleByIngredient
from domain.entities.stop_sale_by_sales_channel import StopSaleBySalesChannel
from domain.entities.stop_sale_by_sector import StopSaleBySector


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

    async def get_units_sales(
        self,
        *,
        access_token: str,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        unit_ids: Iterable[UUID],
    ) -> list[UnitSales]: ...

    async def get_production_productivity(
        self,
        *,
        access_token: str,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        unit_ids: Iterable[UUID],
    ) -> list[UnitProductionProductivity]: ...

    async def get_stop_sales_by_sales_channels(
        self,
        *,
        access_token: str,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        unit_ids: Iterable[UUID],
    ) -> list[StopSaleBySalesChannel]: ...

    async def get_stop_sales_by_ingredients(
        self,
        *,
        access_token: str,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        unit_ids: Iterable[UUID],
    ) -> list[StopSaleByIngredient]: ...

    async def get_stop_sales_by_sectors(
        self,
        *,
        access_token: str,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        unit_ids: Iterable[UUID],
    ) -> list[StopSaleBySector]: ...
