from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from domain.entities.account_token import AccountTokenUnits
from domain.entities.unit import Unit


@dataclass(frozen=True, slots=True)
class AccountTokenUnitsService:
    account_token_units: Iterable[AccountTokenUnits]

    def get_units(self) -> list[Unit]:
        """
        Returns a list of units from the account token units.
        """
        return [
            unit
            for account_token_units in self.account_token_units
            for unit in account_token_units.units
        ]

    def get_unit_id_to_name(self) -> dict[UUID, str]:
        """
        Returns a dictionary mapping unit IDs to unit names.
        """
        return {unit.id: unit.name for unit in self.get_units()}
