from pydantic import BaseModel, SecretStr

from domain.entities.unit import Unit


class AccountToken(BaseModel):
    account_id: str
    access_token: SecretStr


class AccountTokenUnits(AccountToken):
    units: list[Unit]
