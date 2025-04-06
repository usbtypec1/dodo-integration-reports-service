import datetime
from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, Field


class LateDeliveryVoucher(BaseModel):
    order_id: Annotated[UUID, Field(validation_alias="orderId")]
    order_number: Annotated[str, Field(validation_alias="orderNumber")]
    order_accepted_at_local: Annotated[
        datetime.datetime,
        Field(validation_alias="orderAcceptedAtLocal"),
    ]
    unit_id: Annotated[UUID, Field(validation_alias="unitId")]
    predicted_delivery_time_local: Annotated[
        datetime.datetime,
        Field(validation_alias="predictedDeliveryTimeLocal"),
    ]
    order_fulfilment_flag_at_local: Annotated[
        datetime.datetime | None,
        Field(validation_alias="orderFulfilmentFlagAtLocal"),
    ]
    delivery_deadline_local: Annotated[
        datetime.datetime,
        Field(validation_alias="deliveryDeadlineLocal"),
    ]
    issuer_name: Annotated[str | None, Field(validation_alias="issuerName")]
    courier_staff_id: Annotated[
        UUID | None,
        Field(validation_alias="courierStaffId"),
    ]


class LateDeliveryVouchersResponse(BaseModel):
    vouchers: list[LateDeliveryVoucher]
    is_end_of_list_reached: Annotated[
        bool,
        Field(validation_alias="isEndOfListReached"),
    ]


class UnitLateDeliveryVouchersReport(BaseModel):
    unit_name: str
    vouchers_count_for_today: int
    vouchers_count_for_week_before: int
