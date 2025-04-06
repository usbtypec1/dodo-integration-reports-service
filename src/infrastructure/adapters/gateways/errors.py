import logging

import httpx

from infrastructure.exceptions.gateways.dodo_is_api import DodoIsApiGatewayEror

logger = logging.getLogger(__name__)


def handle_dodo_is_api_gateway_errors(response: httpx.Response) -> None:
    if response.is_success:
        return
    raise DodoIsApiGatewayEror(response.text)
