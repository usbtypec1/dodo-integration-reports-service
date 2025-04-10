from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class UnitSales(BaseModel):
    unit_id: Annotated[UUID, Field(validation_alias="unitId")]
    sales: float
    orders_count: Annotated[int, Field(validation_alias="ordersCount")]


class UnitSalesStatistics(BaseModel):
    unit_name: str
    sales_for_today: float
    growth_percentage: int


class TotalSalesStatistics(BaseModel):
    sales_for_today: float
    growth_percentage: int


class SalesStatistics(BaseModel):
    units_breakdown: list[UnitSalesStatistics]
    total: TotalSalesStatistics
