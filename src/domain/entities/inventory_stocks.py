import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.enums.category_name import CategoryName
from domain.entities.enums.measurement_unit import MeasurementUnit


class InventoryStockItem(BaseModel):
    id: UUID
    name: str
    unit_id: Annotated[UUID, Field(validation_alias="unitId")]
    category_name: Annotated[
        CategoryName,
        Field(validation_alias="categoryName"),
    ]
    quantity: int
    measurement_unit: Annotated[
        MeasurementUnit,
        Field(validation_alias="measurementUnit"),
    ]
    balance_in_money: Annotated[float, Field(validation_alias="balanceInMoney")]
    currency: str
    average_weekday_expense: Annotated[
        float,
        Field(validation_alias="avgWeekdayExpense"),
    ]
    average_weekend_expense: Annotated[
        float,
        Field(validation_alias="avgWeekendExpense"),
    ]
    days_until_balance_runs_out: Annotated[
        int,
        Field(validation_alias="daysUntilBalanceRunsOut"),
    ]
    calculated_at: Annotated[
        datetime.datetime,
        Field(validation_alias="calculatedAt"),
    ]


class InventoryStocksResponse(BaseModel):
    stocks: list[InventoryStockItem]
    is_end_of_list_reached: Annotated[
        bool,
        Field(validation_alias="isEndOfListReached"),
    ]
