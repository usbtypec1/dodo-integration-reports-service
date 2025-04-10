from uuid import UUID

from pydantic import BaseModel


class UnitRoute(BaseModel):
    unit_id: UUID
    chat_ids: tuple[int, ...]
    report_type_id: str
