from collections.abc import Iterable
from dataclasses import dataclass

from application.interactors.late_delivery_voucher_list import (
    LateDeliveryVoucherListInteractor,
)
from application.ports.gateways.dodo_is_api import DodoIsApiGateway
from domain.entities.account_token import AccountTokenUnits
from domain.entities.late_delivery_voucher import (
    UnitLateDeliveryVouchersReport,
)
from domain.entities.period import Period
from domain.services.late_delivery_vouchers import (
    generate_late_delivery_vouchers_report,
)
from domain.services.unit import UnitService


@dataclass(frozen=True, slots=True, kw_only=True)
class LateDeliveryVouchersReportInteractor:
    dodo_is_api_gateway: DodoIsApiGateway
    account_tokens_units: Iterable[AccountTokenUnits]

    async def execute(self) -> list[UnitLateDeliveryVouchersReport]:
        period_today = Period.today_to_this_time()
        period_week_before = Period.week_before_to_this_time()

        result: list[UnitLateDeliveryVouchersReport] = []
        for account_token_units in self.account_tokens_units:
            unit_service = UnitService(units=account_token_units.units)
            late_delivery_vouchers_for_today = await LateDeliveryVoucherListInteractor(
                from_date=period_today.from_date,
                to_date=period_today.to_date,
                dodo_is_api_gateway=self.dodo_is_api_gateway,
                unit_ids=unit_service.get_unit_ids(),
                access_token=account_token_units.access_token.get_secret_value(),
            ).execute()
            late_delivery_vouchers_for_week_before = (
                await LateDeliveryVoucherListInteractor(
                    from_date=period_week_before.from_date,
                    to_date=period_week_before.to_date,
                    dodo_is_api_gateway=self.dodo_is_api_gateway,
                    unit_ids=unit_service.get_unit_ids(),
                    access_token=account_token_units.access_token.get_secret_value(),
                ).execute()
            )

            result += generate_late_delivery_vouchers_report(
                units=unit_service.units,
                vouchers_for_today=late_delivery_vouchers_for_today,
                vouchers_for_week_before=late_delivery_vouchers_for_week_before,
            )

        return result
