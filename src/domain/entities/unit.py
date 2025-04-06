from uuid import UUID

from pydantic import BaseModel


class Unit(BaseModel):
    id: UUID
    name: str
    dodo_is_api_account_id: str | None
