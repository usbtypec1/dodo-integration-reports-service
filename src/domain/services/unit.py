from collections.abc import Iterable
from collections import defaultdict
from dataclasses import dataclass
from uuid import UUID

from domain.entities.account_token import AccountToken, AccountTokenUnits
from domain.entities.unit import Unit


@dataclass(frozen=True, slots=True, kw_only=True)
class UnitService:
    units: Iterable[Unit]

    def group_by_dodo_is_api_account_id(self) -> dict[str, list[Unit]]:
        grouped_units: defaultdict[str, list[Unit]] = defaultdict(list)
        for unit in self.units:
            if unit.dodo_is_api_account_id is None:
                continue
            grouped_units[unit.dodo_is_api_account_id].append(unit)
        return grouped_units

    def get_dodo_is_api_account_ids(self) -> set[str]:
        return {
            unit.dodo_is_api_account_id
            for unit in self.units
            if unit.dodo_is_api_account_id is not None
        }

    def get_unit_ids(self) -> set[UUID]:
        return {unit.id for unit in self.units}

    def combine_with_account_tokens(
        self,
        account_tokens: Iterable[AccountToken],
    ) -> list[AccountTokenUnits]:
        account_id_to_token = {
            token.account_id: token.access_token for token in account_tokens
        }

        result: list[AccountTokenUnits] = []
        for account_id, units in self.group_by_dodo_is_api_account_id().items():
            try:
                access_token = account_id_to_token[account_id]
            except KeyError:
                continue

            result.append(
                AccountTokenUnits(
                    account_id=account_id,
                    access_token=access_token,
                    units=units,
                )
            )

        return result
