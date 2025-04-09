import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.enums.channel_stop_type import ChannelStopType
from domain.entities.enums.sales_channel_name import SalesChannelName


class StopSaleBySalesChannel(BaseModel):
    id: UUID
    unit_id: Annotated[UUID, Field(validation_alias="unitId")]
    unit_name: Annotated[str, Field(validation_alias="unitName")]
    sales_channel_name: Annotated[
        SalesChannelName,
        Field(validation_alias="salesChannelName"),
    ]
    reason: Annotated[str, Field(validation_alias="reason")]
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
    channel_stop_type: Annotated[
        ChannelStopType,
        Field(validation_alias="channelStopType"),
    ]


class UnitStopSaleBySalesChannel(BaseModel):
    unit_name: str
    started_at: datetime.datetime
    sales_channel_name: SalesChannelName
    reason: str
