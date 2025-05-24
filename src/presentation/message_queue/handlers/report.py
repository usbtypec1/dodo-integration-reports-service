from typing import Any

from faststream.redis import RedisRouter
from pydantic import BaseModel

from application.interactors.account_token_list import (
    AccountTokenListInteractor,
)
from application.interactors.chat_route_list import ChatRouteListInteractor
from application.interactors.late_delivery_vouchers_report import (
    LateDeliveryVouchersReportInteractor,
)
from application.interactors.production_productivity import (
    ProductionProductivityInteractor,
)
from application.interactors.running_out_inventory_stocks import (
    RunningOutInventoryStocksInteractor,
)
from application.interactors.stop_sales_by_ingredients import (
    StopSalesByIngredientsInteractor,
)
from application.interactors.stop_sales_by_sales_channels import (
    StopSalesBySalesChannelsInteractor,
)
from application.interactors.stop_sales_by_sectors import (
    StopSalesBySectorsInteractor,
)
from application.interactors.unit_list import UnitListInteractor
from application.interactors.units_sales import UnitsSalesStatisticsInteractor
from infrastructure.providers.config import ConfigDependency
from infrastructure.providers.gateways.account_tokens import (
    AccountTokenGatewayDependency,
)
from infrastructure.providers.gateways.dodo_is_api import (
    DodoIsApiGatewayDependency,
)
from infrastructure.providers.gateways.report_route import (
    ReportRouteGatewayDependency,
)
from infrastructure.providers.gateways.unit import UnitGatewayDependency


class IncomingReportEvent(BaseModel):
    report_type_id: str
    chat_ids: set[int]


class OutgoingReportEvent(BaseModel):
    report_type_id: str
    chat_ids: set[int]
    payload: Any


router = RedisRouter()


@router.subscriber("reports")
@router.publisher("reports-router")
async def on_report(
    event: IncomingReportEvent,
    dodo_is_api_gateway: DodoIsApiGatewayDependency,
    report_route_gateway: ReportRouteGatewayDependency,
    unit_gateway: UnitGatewayDependency,
    account_token_gateway: AccountTokenGatewayDependency,
    config: ConfigDependency,
):
    chat_routes = await ChatRouteListInteractor(
        report_route_gateway=report_route_gateway,
        report_type_id=event.report_type_id,
        chat_ids=event.chat_ids,
    ).execute()
    units = await UnitListInteractor(unit_gateway=unit_gateway).execute()
    account_tokens_units = await AccountTokenListInteractor(
        units=units,
        chat_routes=chat_routes,
        account_token_gateway=account_token_gateway,
    ).execute()

    if event.report_type_id == "late_delivery_vouchers":
        reports = await LateDeliveryVouchersReportInteractor(
            dodo_is_api_gateway=dodo_is_api_gateway,
            account_tokens_units=account_tokens_units,
            timezone=config.timezone,
        ).execute()
    elif event.report_type_id == "inventory_stocks":
        reports = await RunningOutInventoryStocksInteractor(
            dodo_is_api_gateway=dodo_is_api_gateway,
            account_tokens_units=account_tokens_units,
        ).execute()
    elif event.report_type_id == "sales":
        reports = await UnitsSalesStatisticsInteractor(
            dodo_is_api_gateway=dodo_is_api_gateway,
            account_tokens_units=account_tokens_units,
            timezone=config.timezone,
        ).execute()
    elif event.report_type_id == "production_productivity":
        reports = await ProductionProductivityInteractor(
            dodo_is_api_gateway=dodo_is_api_gateway,
            account_tokens_units=account_tokens_units,
            timezone=config.timezone,
        ).execute()
    elif event.report_type_id == "stop_sales_by_sectors":
        reports = await StopSalesBySectorsInteractor(
            dodo_is_api_gateway=dodo_is_api_gateway,
            account_tokens_units=account_tokens_units,
            timezone=config.timezone,
        ).execute()
    elif event.report_type_id == "stop_sales_by_ingredients":
        reports = await StopSalesByIngredientsInteractor(
            dodo_is_api_gateway=dodo_is_api_gateway,
            account_tokens_units=account_tokens_units,
            timezone=config.timezone,
        ).execute()
    elif event.report_type_id == "stop_sales_by_sales_channels":
        reports = await StopSalesBySalesChannelsInteractor(
            dodo_is_api_gateway=dodo_is_api_gateway,
            account_tokens_units=account_tokens_units,
            timezone=config.timezone,
        ).execute()
    else:
        raise ValueError(f"Unknown report type: {event.report_type_id}")
    return OutgoingReportEvent(
        report_type_id=event.report_type_id,
        chat_ids=event.chat_ids,
        payload=reports,
    )
