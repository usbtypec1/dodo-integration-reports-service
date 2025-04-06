from collections import Counter
from collections.abc import Iterable

from domain.entities.unit import Unit
from domain.entities.late_delivery_voucher import (
    LateDeliveryVoucher,
    UnitLateDeliveryVouchersReport,
)


def generate_late_delivery_vouchers_report(
    units: Iterable[Unit],
    vouchers_for_today: Iterable[LateDeliveryVoucher],
    vouchers_for_week_before: Iterable[LateDeliveryVoucher],
) -> list[UnitLateDeliveryVouchersReport]:
    unit_id_to_count_for_today = Counter(
        voucher.unit_id for voucher in vouchers_for_today
    )
    unit_id_to_count_for_week_before = Counter(
        voucher.unit_id for voucher in vouchers_for_week_before
    )

    result: list[UnitLateDeliveryVouchersReport] = []
    for unit in units:
        count_for_today = unit_id_to_count_for_today.get(unit.id, 0)
        count_for_week_before = unit_id_to_count_for_week_before.get(unit.id, 0)

        result.append(
            UnitLateDeliveryVouchersReport(
                unit_name=unit.name,
                vouchers_count_for_today=count_for_today,
                vouchers_count_for_week_before=count_for_week_before,
            )
        )

    return result
