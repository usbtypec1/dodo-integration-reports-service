from fast_depends import inject
from faststream.redis import RedisBroker
from pydantic import BaseModel

from application.interactors.late_delivery_vouchers_report import (
    LateDeliveryVouchersReportInteractor,
)
from bootstrap.config import load_config_from_file
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

broker = RedisBroker(load_config_from_file().message_queue_url)


class ReportEvent(BaseModel):
    report_type_id: str
    chat_id: int


@broker.subscriber("reports")
@inject
async def on_report(
    event: ReportEvent,
    dodo_is_api_gateway: DodoIsApiGatewayDependency,
    report_route_gateway: ReportRouteGatewayDependency,
    unit_gateway: UnitGatewayDependency,
    account_token_gateway: AccountTokenGatewayDependency,
):
    reports = await LateDeliveryVouchersReportInteractor(
        unit_gateway=unit_gateway,
        account_token_gateway=account_token_gateway,
        dodo_is_api_gateway=dodo_is_api_gateway,
    ).execute()
    print(reports)
