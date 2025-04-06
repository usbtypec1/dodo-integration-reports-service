from dataclasses import dataclass
import datetime
from collections.abc import Iterable
from uuid import UUID

from domain.entities.late_delivery_voucher import LateDeliveryVouchersResponse
from infrastructure.adapters.gateways.errors import (
    handle_dodo_is_api_gateway_errors,
)
from infrastructure.adapters.gateways.http_client import (
    DodoIsApiGatewayHttpClient,
)


def join_unit_ids(unit_ids: Iterable[UUID]) -> str:
    """
    Join unit IDs into a comma-separated string.

    Args:
        unit_ids (Iterable[UUID]): List of unit IDs.

    Returns:
        str: Comma-separated string of unit IDs.
    """
    return ",".join(unit_id.hex for unit_id in unit_ids)


@dataclass(frozen=True, slots=True)
class DodoIsApiGateway:
    http_client: DodoIsApiGatewayHttpClient

    async def get_late_delivery_vouchers(
        self,
        *,
        access_token: str,
        from_date: datetime.datetime,
        to_date: datetime.datetime,
        unit_ids: Iterable[UUID],
        take: int | None = None,
        skip: int | None = None,
    ) -> LateDeliveryVouchersResponse:
        """
        Get late delivery vouchers from Dodo IS API.

        Keyword Args:
            access_token (str): Access token for authentication.
            from_date (datetime): Start date for the query.
            to_date (datetime): End date for the query.
            unit_ids (Iterable[UUID]): List of unit IDs to filter by.
            take (int | None): Number of records to take.
            skip (int | None): Number of records to skip.

        Returns:
            List of late delivery vouchers.
        """
        url = "/delivery/vouchers"
        query_params: dict = {
            "from": f"{from_date:%Y-%m-%dT%H:%M:%S}",
            "to": f"{to_date:%Y-%m-%dT%H:%M:%S}",
            "units": join_unit_ids(unit_ids),
        }
        if take is not None:
            query_params["take"] = take
        if skip is not None:
            query_params["skip"] = skip
        headers = {"Authorization": f"Bearer {access_token}"}

        response = await self.http_client.get(
            url=url,
            params=query_params,
            headers=headers,
        )
        handle_dodo_is_api_gateway_errors(response)
        return LateDeliveryVouchersResponse.model_validate_json(response.text)
