from typing import Protocol

from domain.entities.unit import Unit


class UnitGateway(Protocol):
    async def get_units(self) -> list[Unit]: ...
