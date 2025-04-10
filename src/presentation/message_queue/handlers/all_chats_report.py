from typing import Any

from pydantic import BaseModel

from application.interactors.account_token_list import (
    AccountTokenListInteractor,
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
from application.interactors.unit_route_list import (
    UnitRouteListInteractor,
)
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
from presentation.message_queue.handlers.broker import broker


class IncomingReportEvent(BaseModel):
    report_type_id: str


class OutgoingReportEvent(BaseModel):
    report_type_id: str
    chat_ids: set[int]
    payload: Any


@broker.subscriber("all-chats-report")
async def on_report(
    event: IncomingReportEvent,
    dodo_is_api_gateway: DodoIsApiGatewayDependency,
    report_route_gateway: ReportRouteGatewayDependency,
    unit_gateway: UnitGatewayDependency,
    account_token_gateway: AccountTokenGatewayDependency,
    config: ConfigDependency,
):
    publisher = broker.publisher("reports-router")
    unit_routes = await UnitRouteListInteractor(
        report_route_gateway=report_route_gateway,
        report_type_id=event.report_type_id,
    ).execute()
    units = await UnitListInteractor(unit_gateway=unit_gateway).execute()
    account_tokens_units = await AccountTokenListInteractor(
        units=units,
        account_token_gateway=account_token_gateway,
    ).execute()
    if event.report_type_id == "inventory_stocks":
        reports = await RunningOutInventoryStocksInteractor(
            dodo_is_api_gateway=dodo_is_api_gateway,
            account_tokens_units=account_tokens_units,
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
        raise ValueError(f"Unknown report type {event.report_type_id}")

    unit_id_to_chat_ids = {
        unit_route.unit_id: unit_route.chat_ids for unit_route in unit_routes
    }
    for report in reports:
        try:
            chat_ids = unit_id_to_chat_ids[report.unit_id]
        except KeyError:
            continue
        await publisher.publish(
            {
                "chat_ids": chat_ids,
                "report_type_id": event.report_type_id,
                "payload": report,
            }
        )
