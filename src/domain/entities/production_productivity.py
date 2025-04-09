from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class UnitProductionProductivity(BaseModel):
    unit_id: Annotated[UUID, Field(validation_alias="unitId")]
    unit_name: Annotated[str, Field(validation_alias="unitName")]
    labor_hours: Annotated[float, Field(validation_alias="laborHours")]
    sales: float
    sales_per_labor_hour: Annotated[
        float,
        Field(validation_alias="salesPerLaborHour"),
    ]
    products_per_labor_hour: Annotated[
        float,
        Field(validation_alias="productsPerLaborHour"),
    ]
    average_heated_shelf_time: Annotated[
        int,
        Field(validation_alias="avgHeatedShelfTime"),
    ]
    orders_per_courier_labor_hour: Annotated[
        float,
        Field(validation_alias="ordersPerCourierLabourHour"),
    ]


class UnitProductionProductivityStatistics(BaseModel):
    unit_name: str
    sales_per_labor_hour_for_today: float
    growth_percentage: int
