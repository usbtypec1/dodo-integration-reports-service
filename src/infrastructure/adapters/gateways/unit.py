from dataclasses import dataclass

from pydantic import TypeAdapter

from domain.entities.unit import Unit
from infrastructure.adapters.gateways.http_client import ApiGatewayHttpClient


@dataclass(frozen=True, slots=True, kw_only=True)
class UnitGateway:
    http_client: ApiGatewayHttpClient

    async def get_units(self) -> list[Unit]:
        url = "/v1/units/"
        response = await self.http_client.get(url)
        type_adapter = TypeAdapter(list[Unit])
        response_data = response.json()
        return type_adapter.validate_python(response_data["units"])
