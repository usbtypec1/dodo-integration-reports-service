import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.enums.ingredient_category_name import (
    IngredientCategoryName,
)


class StopSaleByIngredient(BaseModel):
    id: UUID
    unit_id: Annotated[UUID, Field(validation_alias="unitId")]
    unit_name: Annotated[str, Field(validation_alias="unitName")]
    ingredient_id: Annotated[UUID, Field(validation_alias="ingredientId")]
    ingredient_name: Annotated[str, Field(validation_alias="ingredientName")]
    ingredient_category_name: Annotated[
        IngredientCategoryName,
        Field(validation_alias="ingredientCategoryName"),
    ]
    reason: str
    started_at_local: Annotated[
        datetime.datetime,
        Field(validation_alias="startedAtLocal"),
    ]
    ended_at_local: Annotated[
        datetime.datetime | None,
        Field(validation_alias="endedAtLocal"),
    ]
    stopped_by_user_id: Annotated[
        UUID,
        Field(validation_alias="stoppedByUserId"),
    ]
    resumed_by_user_id: Annotated[
        UUID | None,
        Field(validation_alias="resumedByUserId"),
    ]


class UnitStopSalesByIngredientItem(BaseModel):
    name: str
    started_at: datetime.datetime


class UnitStopSalesByIngredientsByReasons(BaseModel):
    reason: str
    ingredients: list[UnitStopSalesByIngredientItem]


class UnitStopSalesByIngredients(BaseModel):
    unit_id: UUID
    unit_name: str
    ingredients_by_reasons: list[UnitStopSalesByIngredientsByReasons]
    timezone: str
