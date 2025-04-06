from dataclasses import dataclass

from application.ports.gateways.unit import UnitGateway
from domain.entities.unit import Unit


@dataclass(frozen=True, slots=True, kw_only=True)
class UnitListInteractor:
    unit_gateway: UnitGateway

    async def execute(self) -> list[Unit]:
        return await self.unit_gateway.get_units()
