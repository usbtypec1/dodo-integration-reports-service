import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class StopSaleBySector(BaseModel):
    id: UUID
    unit_id: Annotated[UUID, Field(validation_alias="unitId")]
    unit_name: Annotated[str, Field(validation_alias="unitName")]
    sector_name: Annotated[str, Field(validation_alias="sectorName")]
    is_sub_sector: Annotated[bool, Field(validation_alias="isSubSector")]
    started_at: Annotated[datetime.datetime, Field(validation_alias="startedAt")]
    started_at_local: Annotated[
        datetime.datetime | None,
        Field(validation_alias="startedAtLocal"),
    ]
    ended_at: Annotated[datetime.datetime | None, Field(validation_alias="endedAt")]
    ended_at_local: Annotated[
        datetime.datetime | None,
        Field(validation_alias="endedAtLocal"),
    ]
    suspended_by_user_id: Annotated[
        UUID | None,
        Field(validation_alias="suspendedByUserId"),
    ]
    resumed_user_id: Annotated[
        UUID | None,
        Field(validation_alias="resumedUserId"),
    ]


class UnitStopSaleBySectorItem(BaseModel):
    name: str
    started_at: datetime.datetime


class UnitStopSaleBySector(BaseModel):
    unit_id: UUID
    unit_name: str
    sectors: list[UnitStopSaleBySectorItem]
